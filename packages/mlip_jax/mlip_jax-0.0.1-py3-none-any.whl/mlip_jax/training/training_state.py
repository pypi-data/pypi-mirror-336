import logging
import time
from dataclasses import field
from typing import Optional

import chex
import jax
import optax
from flax.struct import dataclass as flax_dataclass

from mlip_jax.models.type_aliases import ModelParameters
from mlip_jax.training.ema import EMAParameterTransformation, EMAState


@flax_dataclass
class TrainingState:
    """
    Represents the state of training.

    Attributes:
        params: Model parameters.
        optimizer_state: State of the optimizer.
        ema_state: Exponentially weighted average state.
        num_steps: The number of training steps taken.
        acc_steps: The number of gradient accumulation steps taken; resets to 0 after
                   each optimizer step.
        key: Pseudo-random number generator key.
        extras: Additional auxiliary information in form of a dictionary.
    """

    params: ModelParameters
    optimizer_state: optax.OptState
    ema_state: EMAState
    num_steps: jax.Array
    acc_steps: jax.Array
    key: chex.PRNGKey
    extras: Optional[dict] = field(default_factory=dict)


def _count_parameters(params: ModelParameters) -> int:
    return sum(x.size for x in jax.tree_util.tree_leaves(params))


def init_training_state(
    initial_params: ModelParameters,
    random_key: chex.PRNGKey,
    optimizer: optax.GradientTransformation,
    ema_fun: EMAParameterTransformation,
) -> TrainingState:
    """Initializes the training state.

    Args:
        initial_params: The initial parameters.
        random_key: A jax-compatible random key.
        optimizer: The optimizer.
        ema_fun: The EMA parameter transformation function.

    Returns:
        The initialized training state.
    """
    key, gnn_key = jax.random.split(random_key, 2)
    cpu_device = jax.devices("cpu")[0]
    start_time = time.perf_counter()

    with jax.default_device(cpu_device):
        opt_state = optimizer.init(initial_params)
        ema_state = ema_fun.init(initial_params)

        training_state = TrainingState(
            params=initial_params,
            optimizer_state=opt_state,
            ema_state=ema_state,
            num_steps=0,
            acc_steps=0,
            key=key,
            extras={},
        )

        logging.info(
            "Prepared training state on CPU in %.2f sec.",
            time.perf_counter() - start_time,
        )
        logging.info("Number of parameters: %s", _count_parameters(initial_params))
        logging.info(
            "Number of parameters in optimizer: %s", _count_parameters(opt_state)
        )

    return training_state
