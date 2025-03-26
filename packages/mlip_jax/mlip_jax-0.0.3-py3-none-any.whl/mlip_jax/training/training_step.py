import functools
from typing import Callable, Optional

import jax
import jraph
import optax

from mlip_jax.training.ema import EMAParameterTransformation
from mlip_jax.training.training_state import TrainingState


def _training_step(
    training_state: TrainingState,
    graph: jraph.GraphsTuple,
    epoch_number: int,
    loss_fun: Callable,
    optimizer: optax.GradientTransformation,
    ema_fun: EMAParameterTransformation,
    num_gradient_accumulation_steps: Optional[int],
    should_parallelize: bool,
) -> tuple[TrainingState, dict]:
    # Fetch params and optimizer state from training state.
    params = training_state.params
    optimizer_state = training_state.optimizer_state
    ema_state = training_state.ema_state
    num_steps = training_state.num_steps
    acc_steps = training_state.acc_steps
    key = training_state.key

    # Calculate gradients.
    grad_fun = jax.grad(loss_fun, argnums=0, has_aux=True)

    key, _ = jax.random.split(key, 2)

    grads, aux_info = grad_fun(params, graph, epoch_number)

    # Aggregrate over devices.
    if should_parallelize:
        grads = jax.lax.pmean(grads, axis_name="device")

    # Gradient step on params.
    updates, optimizer_state = optimizer.update(grads, optimizer_state, params=params)
    params = optax.apply_updates(params, updates)

    # Fetch logging info from aux_info.
    metrics = aux_info

    # Add batch-level metrics to the dictionary.
    metrics["gradient_norm"] = optax.global_norm(grads)
    metrics["param_update_norm"] = optax.global_norm(updates)

    # Aggregrate over global devices.
    if should_parallelize:
        metrics = jax.lax.pmean(metrics, axis_name="device")

    # Update per-step variables.
    acc_steps = (acc_steps + 1) % num_gradient_accumulation_steps
    ema_state = jax.lax.cond(
        acc_steps == 0, lambda x: ema_fun.update(x, params), lambda x: x, ema_state
    )
    num_steps = jax.lax.cond(acc_steps == 0, lambda x: x + 1, lambda x: x, num_steps)

    # Preprate new training state.
    training_state = TrainingState(
        params=params,
        optimizer_state=optimizer_state,
        ema_state=ema_state,
        key=key,
        num_steps=num_steps,
        acc_steps=acc_steps,
        extras=training_state.extras,
    )

    return training_state, metrics


def make_train_step(
    loss_fun: Callable,
    optimizer: optax.GradientTransformation,
    ema_fun: EMAParameterTransformation,
    num_gradient_accumulation_steps: Optional[int] = 1,
    should_parallelize: bool = True,
) -> Callable:
    """
    Create a training step function to optimize model params using gradients.

    Args:
        loss_fun: A function that computes the loss, taking model params,
                  batch data, a random key, and other optional params as input.
        optimizer: An optimizer for updating model params based on computed gradients.
        ema_fun: A function for updating the exponential moving average (EMA) of
                 the model params.
        num_gradient_accumulation_steps: The number of gradient accumulation
                                         steps before a parameter update is performed.
                                         Defaults to 1, implying immediate updates.
        should_parallelize: Whether to apply pmap.

    Returns:
        A function that takes the current training state and a batch of data as
        input, and returns the updated training state along with training metrics.
    """
    training_step = functools.partial(
        _training_step,
        loss_fun=loss_fun,
        optimizer=optimizer,
        ema_fun=ema_fun,
        num_gradient_accumulation_steps=num_gradient_accumulation_steps,
        should_parallelize=should_parallelize,
    )

    if should_parallelize:
        return jax.pmap(
            training_step,
            axis_name="device",
            donate_argnums=(0,),
            static_broadcasted_argnums=2,
        )
    return jax.jit(training_step, donate_argnums=(0,))
