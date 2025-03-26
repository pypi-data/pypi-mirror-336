from typing import Callable

import optax

from mlip_jax.training.optimizer_config import OptimizerConfig
from mlip_jax.utils.dict_flatten import flatten_dict, unflatten_dict


# This following function is needed for MACE
def _weight_decay_mask(params: optax.Params):
    params = flatten_dict(params)
    mask = {
        k: any(("linear_down" in ki) or ("SymmetricContraction" in ki) for ki in k)
        for k in params
    }
    assert any(any(("linear_down" in ki) for ki in k) for k in params)
    assert any(any(("SymmetricContraction" in ki) for ki in k) for k in params)
    return unflatten_dict(mask)


def init_optimizer(
    base_optimizer_factory_fun: Callable[[float], optax.GradientTransformation],
    config: OptimizerConfig,
) -> optax.GradientTransformation:
    """Initializes the optimizer (based on optax).

    The initialization happens from a base optimizer function, for example,
    optax.adam. This base optimizer function must be able to take in the learning rate
    as a single parameter.

    The return value of this is a full optimizer pipeline consisting of
    gradient clipping, warm-up, etc.

    Args:
        base_optimizer_factory_fun: The base optimizer function which must be able to
                                    take in the learning rate as a single parameter.
        config: The optimizer pydantic config.

    Returns:
        The full optimizer pipeline constructed based on the provided
        base optimizer function.
    """
    if config.apply_weight_decay_mask:
        weight_decay_transform = optax.add_decayed_weights(
            config.weight_decay, _weight_decay_mask
        )
    else:
        weight_decay_transform = optax.add_decayed_weights(config.weight_decay)

    return optax.inject_hyperparams(
        lambda lr: optax.MultiSteps(
            optax.chain(
                weight_decay_transform,
                optax.clip_by_global_norm(config.grad_norm),
                base_optimizer_factory_fun(lr),
            ),
            every_k_schedule=config.num_gradient_accumulation_steps,
        )
    )(
        lr=optax.join_schedules(
            schedules=[
                optax.linear_schedule(
                    init_value=config.init_learning_rate,
                    end_value=config.peak_learning_rate,
                    transition_steps=config.warmup_steps,
                ),
                optax.linear_schedule(
                    init_value=config.peak_learning_rate,
                    end_value=config.final_learning_rate,
                    transition_steps=config.transition_steps,
                ),
            ],
            boundaries=[config.warmup_steps],
        ),
    )
