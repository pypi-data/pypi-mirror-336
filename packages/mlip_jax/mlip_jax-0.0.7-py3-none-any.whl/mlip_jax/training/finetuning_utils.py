from typing import TypeAlias

import jax
import jax.numpy as jnp
import optax

from mlip_jax.models.type_aliases import ModelParameters
from mlip_jax.utils.dict_flatten import flatten_dict, unflatten_dict

OptimizerMask: TypeAlias = dict[str, dict[str, bool | dict]]


def _create_finetuning_mask_for_optimizer(
    params: ModelParameters, finetuning_blocks: list[str]
) -> OptimizerMask:
    flattened_params = flatten_dict(params)
    mask = {
        k: any(finetuning_block in k for finetuning_block in finetuning_blocks)
        for k in flattened_params
    }
    return unflatten_dict(mask)


def _zero_grads():
    def init_fn(_):
        return ()

    def update_fn(updates, state, params=None):
        return jax.tree_map(jnp.zeros_like, updates), ()

    return optax.GradientTransformation(init_fn, update_fn)


def mask_optimizer_for_finetuning(
    optimizer: optax.GradientTransformation,
    params: ModelParameters,
    finetuning_blocks: list[str],
):
    """Masks a given optimizer for fine-tuning tasks, where only the new readout heads
    are updated.

    Args:
        optimizer: The base optimizer to mask.
        params: The parameters.
        finetuning_blocks: A list of names for those blocks in the parameters that
                           should be updated during fine-tuning.

    Returns:
        The masked optimizer.
    """
    assert len(finetuning_blocks) > 0
    mask = _create_finetuning_mask_for_optimizer(params, finetuning_blocks)

    # First, we need to apply a mask to get rid of unnecessary parameters in optimizer
    optimizer = optax.masked(optimizer, mask)

    # We also need to zero-out gradients of other parameters
    # See: https://github.com/google-deepmind/optax/discussions/167
    return optax.multi_transform({True: optimizer, False: _zero_grads()}, mask)
