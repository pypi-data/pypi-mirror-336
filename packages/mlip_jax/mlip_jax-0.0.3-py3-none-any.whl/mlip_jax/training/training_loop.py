import dataclasses
import logging
import time
from typing import Callable, TypeAlias

import flax
import jax
import jraph
import numpy as np
import optax

from mlip_jax.data.dataset_info import DatasetInfo
from mlip_jax.data.helpers.data_prefetching import PrefetchIterator
from mlip_jax.data.helpers.graph_data_manager import GraphDataManager
from mlip_jax.models.type_aliases import ModelParameters
from mlip_jax.training.ema import exponentially_moving_average
from mlip_jax.training.evaluation import (
    LossFunction,
    make_evaluation_step,
    run_evaluation,
)
from mlip_jax.training.training_io_handler import LogCategory, TrainingIOHandler
from mlip_jax.training.training_loop_config import TrainingLoopConfig
from mlip_jax.training.training_state import TrainingState, init_training_state
from mlip_jax.training.training_step import make_train_step

Optimizer: TypeAlias = optax.GradientTransformation
GraphDataManagerOrPrefetchIterator: TypeAlias = GraphDataManager | PrefetchIterator
TrainingStepFun: TypeAlias = Callable[
    [TrainingState, jraph.GraphsTuple],
    tuple[TrainingState, dict],
]


@dataclasses.dataclass
class LossFunctions:
    """Simple container to hold the two loss functions.

    Attributes:
        training_loss_fun: The loss function for the parameter update step.
        eval_loss_fun: The loss function for the model evaluation step.
    """

    training_loss_fun: LossFunction
    eval_loss_fun: LossFunction


class TrainingLoop:
    """Training loop class.

    It implements only the loop based on its inputs but does not construct any
    auxiliary objects within it. For example, the model, dataset, and optimizer must
    be passed to this function from the outside.

    Attributes:
        training_state: The training state.
    """

    def __init__(
        self,
        train_dataset: GraphDataManagerOrPrefetchIterator,
        validation_dataset: GraphDataManagerOrPrefetchIterator,
        dataset_info: DatasetInfo,
        initial_params: ModelParameters,
        loss_functions: LossFunctions,
        optimizer: Optimizer,
        config: TrainingLoopConfig,
        io_handler: TrainingIOHandler,
        should_parallelize: bool = False,
    ) -> None:
        """Constructor.

        Args:
            train_dataset: The training dataset as either a GraphDataManager or
                           a PrefetchIterator.
            validation_dataset: The validation dataset as either a GraphDataManager or
                                a PrefetchIterator.
            dataset_info: The dataset information object.
            initial_params: The initial parameters of the model.
            loss_functions: The loss functions, which is a dataclass holding the train
                            and evaluation loss functions.
            optimizer: The optimizer (based on optax).
            config: The training loop pydantic config.
            io_handler: The IO handler which handles checkpointing
                        and (specialized) logging.
            should_parallelize: Whether to parallelize (using data parallelization)
                                across multiple devices. The default is ``False``.
        """
        self.should_parallelize = should_parallelize

        self.train_dataset = train_dataset
        self.validation_dataset = (
            validation_dataset
            if config.eval_num_graphs is None
            else validation_dataset.subset(config.eval_num_graphs)
        )
        self.total_num_graphs, self.total_num_nodes = (
            self._get_total_number_of_graphs_and_nodes_in_train_set()
        )

        self.dataset_info = dataset_info
        self.initial_params = initial_params
        self.optimizer = optimizer
        self.config = config

        self.io_handler = io_handler
        self.io_handler.save_dataset_info(self.dataset_info)

        self._prepare_training_state_and_ema()
        self.training_step = make_train_step(
            loss_functions.training_loss_fun,
            self.optimizer,
            self.ema_fun,
            config.num_gradient_accumulation_steps,
            should_parallelize,
        )
        self.metrics = None
        self.eval_step = make_evaluation_step(
            loss_functions.eval_loss_fun, should_parallelize
        )

        self.best_evaluation_step = -1
        self.best_evaluation_loss = float("inf")
        self.best_params = None

        self._should_unreplicate_train_batches = (
            not should_parallelize
        ) and isinstance(self.train_dataset, PrefetchIterator)

        self.num_batches = len(self.train_dataset)
        self.steps_per_epoch = self.num_batches
        if should_parallelize:
            self.steps_per_epoch = (
                self.num_batches // len(jax.devices())
            ) // config.num_gradient_accumulation_steps
        self.epoch_number = self._get_epoch_number_from_training_state()

        logging.info(
            "Training loop: Number of batches has been set to: %s", self.num_batches
        )
        logging.info(
            "Training loop: Steps per epoch has been set to: %s", self.steps_per_epoch
        )

    def run(self) -> None:
        """Runs the training loop.

        The final training state can be accessed via its member variable.
        """
        logging.info("Starting training loop...")

        # May not be zero if restored from checkpoint
        if self.epoch_number > 0:
            self.io_handler.log(
                LogCategory.CLEANUP_AFTER_CKPT_RESTORATION, {}, self.epoch_number
            )

        if self.epoch_number == 0 and self.config.run_eval_at_start:
            logging.info("Running initial evaluation...")
            start_time = time.perf_counter()
            self._run_evaluation()
            logging.info(
                "Initial evaluation done in %.2f sec.", time.perf_counter() - start_time
            )

        self.epoch_number += 1
        while self.epoch_number < self.config.num_epochs + 1:
            t_before_train = time.perf_counter()
            self._run_training_epoch()
            logging.info(
                "Parameter updates of epoch %s done, running evaluation next.",
                self.epoch_number,
            )
            t_after_train = time.perf_counter()
            self._run_evaluation()
            t_after_eval = time.perf_counter()

            logging.info(
                "Epoch %s done. Time for parameter updates: %.2f sec.",
                self.epoch_number,
                t_after_train - t_before_train,
            )
            logging.info("Time for evaluation: %.2f sec.", t_after_eval - t_after_train)

            self.epoch_number += 1

        self.io_handler.wait_until_finished()

        logging.info("Training loop completed.")

    def _run_training_epoch(self) -> None:
        start_time = time.perf_counter()
        metrics = []

        for batch in self.train_dataset:
            if self._should_unreplicate_train_batches:
                batch = flax.jax_utils.unreplicate(batch)
            updated_training_state, _metrics = self.training_step(
                self.training_state, batch, self.epoch_number
            )
            self.training_state = updated_training_state
            metrics.append(jax.device_get(_metrics))

        epoch_time_in_seconds = time.perf_counter() - start_time
        self._log_after_training_epoch(
            metrics, self.epoch_number, epoch_time_in_seconds
        )

    def _run_evaluation(self) -> None:
        devices = jax.devices() if self.should_parallelize else None
        eval_loss = run_evaluation(
            self.eval_step,
            self.validation_dataset,
            self.training_state,
            self.epoch_number,
            self.io_handler,
            self.config.ema_decay if self.config.use_ema_params_for_eval else None,
            devices,
        )

        if self.epoch_number == 0:
            self.best_evaluation_loss = eval_loss
            self.best_evaluation_epoch = 0

        elif eval_loss < self.best_evaluation_loss:
            logging.info(
                "New best epoch %s has evaluation loss: %.6f",
                self.epoch_number,
                eval_loss,
            )
            self.best_evaluation_loss = eval_loss
            self.best_evaluation_epoch = self.epoch_number
            self.best_params = self.training_state.params

            self.io_handler.save_checkpoint(
                (
                    flax.jax_utils.unreplicate(self.training_state)
                    if self.should_parallelize
                    else self.training_state
                ),
                self.epoch_number,
            )

        to_log = {
            "best_loss": self.best_evaluation_loss,
            "best_epoch": self.best_evaluation_epoch,
        }
        self.io_handler.log(LogCategory.BEST_MODEL, to_log, self.epoch_number)

    def test(self, test_dataset: GraphDataManagerOrPrefetchIterator) -> None:
        """Run the evaluation on the test dataset.

        Args:
            test_dataset: The test dataset as either a GraphDataManager or
                          a PrefetchIterator.
        """
        devices = jax.devices() if self.should_parallelize else None
        run_evaluation(
            self.eval_step,
            test_dataset,
            self.training_state,
            self.epoch_number,
            self.io_handler,
            self.config.ema_decay if self.config.use_ema_params_for_eval else None,
            devices,
            is_test_set=True,
        )

    def _prepare_training_state_and_ema(self) -> None:
        key = jax.random.PRNGKey(self.config.random_seed)
        self.ema_fun = exponentially_moving_average(self.config.ema_decay)
        key, init_key = jax.random.split(key, 2)

        training_state = init_training_state(
            self.initial_params, init_key, self.optimizer, self.ema_fun
        )

        # The following line only restores the training state if the associated
        # setting in self.io_handler is set to true.
        training_state = self.io_handler.restore_training_state(training_state)

        training_state = jax.device_put(training_state)

        # Ensure that the training state is the same across all hosts.
        # Note that we could add explicit broadcasting as a backup, e.g.
        #   training_state = jax.experimental.multihost_utils.broadcast_one_to_all(
        #             training_state, is_source=jax.process_index() == 0
        #         )
        # but this should not be necessary so for now we just raise errors if a
        # mismatch is found.
        # Note: DISABLED AS IT'S MEMORY INTENSIVE AND BUT LEFT FOR VALIDATION PURPOSES.
        # assert_pytrees_match_across_hosts(training_state)
        # logging.info(f"Training state is identical across all workers.")

        if self.should_parallelize:
            # Distribute training state
            start_time = time.perf_counter()
            training_state = flax.jax_utils.replicate(training_state)
            logging.info(
                "Distributed training state in %.2f sec.",
                time.perf_counter() - start_time,
            )

            # Distribute keys
            start_time = time.perf_counter()
            key, key_state = jax.random.split(key, 2)
            devices = jax.local_devices()
            keys = jax.device_put_sharded(
                list(jax.random.split(key_state, len(devices))),
                devices,
            )
            training_state = training_state.replace(
                key=keys,
                acc_steps=flax.jax_utils.replicate(0),
            )
            logging.info(
                "Distributed keys in %.2f sec.", time.perf_counter() - start_time
            )

        self.training_state = training_state

    def _get_epoch_number_from_training_state(self) -> int:
        return self._get_num_steps_from_training_state() // self.steps_per_epoch

    def _get_num_steps_from_training_state(self) -> int:
        if self.should_parallelize:
            return int(self.training_state.num_steps[0].squeeze().block_until_ready())
        return int(self.training_state.num_steps.squeeze().block_until_ready())

    def _log_after_training_epoch(
        self,
        metrics: list[dict[str, np.ndarray]],
        epoch_number: int,
        epoch_time_in_seconds: float,
    ) -> None:
        _metrics = {}
        for metric_name in metrics[0].keys():
            _metrics[metric_name] = np.mean([m[metric_name] for m in metrics])

        try:
            opt_hyperparams = jax.device_get(
                self.training_state.optimizer_state.hyperparams
            )
            if self.should_parallelize:
                opt_hyperparams = flax.jax_utils.unreplicate(opt_hyperparams)
            _metrics["learning_rate"] = float(opt_hyperparams["lr"])
        except AttributeError:
            pass

        _metrics["epoch_time_in_seconds"] = epoch_time_in_seconds
        _metrics["nodes_per_second"] = self.total_num_nodes / epoch_time_in_seconds
        _metrics["graphs_per_second"] = self.total_num_graphs / epoch_time_in_seconds

        self.io_handler.log(LogCategory.TRAIN_METRICS, _metrics, epoch_number)

        logging.info(
            "Total number of steps after epoch %s: %s",
            epoch_number,
            self._get_num_steps_from_training_state(),
        )

    def _get_total_number_of_graphs_and_nodes_in_train_set(self) -> tuple[int, int]:
        total_num_graphs = 0
        total_num_nodes = 0

        def _batch_generator():
            if isinstance(self.train_dataset, PrefetchIterator):
                for stacked_batch in self.train_dataset:
                    for i in range(stacked_batch.n_node.shape[0]):
                        yield jax.tree_util.tree_map(
                            lambda x, idx=i: x[idx], stacked_batch
                        )
            else:
                for batch in self.train_dataset:
                    yield batch

        for _batch in _batch_generator():
            total_num_graphs += jraph.get_graph_padding_mask(_batch).sum()
            total_num_nodes += jraph.get_node_padding_mask(_batch).sum()

        return total_num_graphs, total_num_nodes
