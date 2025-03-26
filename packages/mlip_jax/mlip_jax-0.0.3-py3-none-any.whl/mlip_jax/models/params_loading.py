import os
from typing import Any, Mapping, Union

import jax
import orbax.checkpoint as ocp
from orbax.checkpoint import CheckpointManager

from mlip_jax.models.type_aliases import ModelParameters
from mlip_jax.training.training_state import TrainingState
from mlip_jax.utils.multihost import single_host_jax_and_orbax


def _restored_state_from_initial_params(
    initial_params: ModelParameters,
    ckpt_manager: CheckpointManager,
    epoch_to_load: int,
    load_ema_params: bool,
) -> Union[Any, Mapping[str, Any]]:
    training_state_template = TrainingState(
        params=initial_params,
        optimizer_state=None,
        ema_state=None,
        num_steps=0,
        acc_steps=0,
        key=None,
        extras={},
    )
    to_restore = {"training_state": ocp.args.PyTreeRestore(training_state_template)}
    if load_ema_params:
        to_restore["params_ema"] = ocp.args.PyTreeRestore(initial_params)
    restored_state = ckpt_manager.restore(
        epoch_to_load, args=ocp.args.Composite(**to_restore)
    )

    return restored_state


def load_parameters_from_checkpoint(
    local_checkpoint_dir: str | os.PathLike,
    initial_params: ModelParameters,
    epoch_to_load: int,
    load_ema_params: bool = False,
) -> ModelParameters:
    """Loads model parameters from a checkpoint.

    Args:
        local_checkpoint_dir: The directory (must be local) where the
                              checkpoints are stored. This directory should contain the
                              subdirectories named after the epoch numbers of the
                              checkpoints.
        initial_params: The initial parameters of the model as a template for loading.
        epoch_to_load: The epoch number to load.
        load_ema_params: Whether to load the EMA parameters instead of the standard
                         ones. By default, this is set to ``False``.

    Returns:
        The loaded model parameters.
    """

    item_names = ["training_state"]
    if load_ema_params:
        item_names.append("params_ema")
    with single_host_jax_and_orbax():
        ckpt_manager = CheckpointManager(
            local_checkpoint_dir,
            item_names=item_names,
        )

    is_old_params_version = False
    cpu_device = jax.devices("cpu")[0]
    with jax.default_device(cpu_device):
        try:
            restored_state = _restored_state_from_initial_params(
                initial_params, ckpt_manager, epoch_to_load, load_ema_params
            )
        except KeyError:
            initial_params = {"params": initial_params["params"]["mlip_network"]}
            restored_state = _restored_state_from_initial_params(
                initial_params, ckpt_manager, epoch_to_load, load_ema_params
            )
            is_old_params_version = True

    if load_ema_params:
        params = restored_state["params_ema"]
    else:
        params = restored_state["training_state"].params

    if is_old_params_version:
        return {"params": {"mlip_network": params["params"]}}
    return params
