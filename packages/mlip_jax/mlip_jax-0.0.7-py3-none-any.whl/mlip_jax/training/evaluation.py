import functools
from typing import Callable, Optional, TypeAlias

import flax
import jax
import jraph
import numpy as np

from mlip_jax.data.helpers.data_prefetching import PrefetchIterator
from mlip_jax.data.helpers.graph_data_manager import GraphDataManager
from mlip_jax.models.type_aliases import ModelParameters
from mlip_jax.training.ema import get_debiased_params
from mlip_jax.training.training_io_handler import LogCategory, TrainingIOHandler
from mlip_jax.training.training_state import TrainingState

EvaluationStepFun: TypeAlias = Callable[
    [ModelParameters, jraph.GraphsTuple, int], dict[str, np.ndarray]
]
LossFunction: TypeAlias = Callable[
    [ModelParameters, jraph.GraphsTuple, int], tuple[np.ndarray, dict[str, np.ndarray]]
]


def _evaluation_step(
    params: ModelParameters,
    graph: jraph.GraphsTuple,
    training_epoch: int,
    eval_loss_fun: LossFunction,
    should_parallelize: bool,
) -> dict[str, np.ndarray]:
    _, metrics = eval_loss_fun(params, graph, training_epoch)

    if should_parallelize:
        metrics = jax.lax.pmean(metrics, axis_name="device")
    return metrics


def make_evaluation_step(
    eval_loss_fun: LossFunction, should_parallelize: bool = True
) -> EvaluationStepFun:
    """Creates the evaluation step function.

    Args:
        eval_loss_fun: The loss function for the evaluation.
        should_parallelize: Whether to apply data parallelization across
                            multiple devices.

    Returns:
        The evaluation step function.
    """
    evaluation_step = functools.partial(
        _evaluation_step,
        eval_loss_fun=eval_loss_fun,
        should_parallelize=should_parallelize,
    )

    if should_parallelize:
        return jax.pmap(
            evaluation_step, axis_name="device", static_broadcasted_argnums=2
        )
    return jax.jit(evaluation_step)


def run_evaluation(
    evaluation_step: EvaluationStepFun,
    eval_dataset: GraphDataManager | PrefetchIterator,
    training_state: TrainingState,
    epoch_number: int,
    io_handler: TrainingIOHandler,
    ema_decay: Optional[float] = None,
    devices: Optional[list[jax.Device]] = None,
    is_test_set: bool = False,
) -> float:
    """Runs a model evaluation on a given dataset.

    Args:
        evaluation_step: The evaluation step function.
        eval_dataset: The dataset on which to evaluate the model.
        training_state: The training state.
        epoch_number: The current epoch number.
        io_handler: The IO handler class that handles the logging of the result.
        ema_decay: The EMA decay value. It can be None, which is the default.
        devices: The jax devices. It can be None if not run in parallel (default).
        is_test_set: Whether the evaluation is done on the test set, i.e.,
                     not during a training run. By default, this is false.

    Returns:
        The mean loss.
    """
    # Determine model params to use based on settings and training epoch.
    if ema_decay is not None and epoch_number > 0:
        if devices is not None:
            params = jax.pmap(
                get_debiased_params, axis_name="device", static_broadcasted_argnums=(1,)
            )(training_state.ema_state, ema_decay)
        else:
            params = get_debiased_params(training_state.ema_state, ema_decay)
    else:
        params = training_state.params

    should_unreplicate_batches = devices is None and isinstance(
        eval_dataset, PrefetchIterator
    )

    metrics = []
    for batch in eval_dataset:
        if should_unreplicate_batches:
            batch = flax.jax_utils.unreplicate(batch)
        _metrics = evaluation_step(params, batch, epoch_number)
        metrics.append(jax.device_get(_metrics))

    to_log = {}
    for metric_name in metrics[0].keys():
        metrics_values = [m[metric_name] for m in metrics]
        if not any(val is None for val in metrics_values):
            to_log[metric_name] = np.mean(metrics_values)

    mean_eval_loss = float(to_log["loss"])

    if is_test_set:
        io_handler.log(LogCategory.TEST_METRICS, to_log, epoch_number)
    else:
        io_handler.log(LogCategory.EVAL_METRICS, to_log, epoch_number)

    return mean_eval_loss
