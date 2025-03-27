import logging
from typing import Optional, Union

import numpy as np

from mlip_jax.data.dataset_info import DatasetInfo
from mlip_jax.data.helpers.atomic_number_table import AtomicNumberTable


def get_atomic_energies(
    atomic_energies_input: Optional[Union[str, dict[int, float]]],
    dataset_info: DatasetInfo,
    num_species: int,
) -> np.ndarray:
    """Converts an input description of atomic energies into the atomic energies array.

    Args:
        atomic_energies_input: A description of the atomic energies strategy. This can
                               be a string 'average' or 'zero', or it can be the
                               atomic energies dictionary.
        dataset_info: The dataset information object that holds the atomic energies
                      dictionary that is used if atomic_energies_input='average'.
        num_species: Number of species for the model.

    Returns:
        The atomic energies as an array of size number of species.
    """
    z_table = AtomicNumberTable(sorted(dataset_info.atomic_energies_map.keys()))

    if atomic_energies_input == "average" or atomic_energies_input is None:
        atomic_energies_dict = {
            z_table.z_to_index(z): energy
            for z, energy in dataset_info.atomic_energies_map.items()
        }
        logging.info(
            f"Computed average atomic energies using least "
            f"squares, taken from dataset info: {atomic_energies_dict}"
        )
        atomic_energies = np.array(
            [atomic_energies_dict[i] for i in range(len(z_table.zs))]
        )
    elif atomic_energies_input == "zero":
        logging.info("Not using atomic energies, setting them to zero.")
        atomic_energies = np.zeros(num_species)
    elif isinstance(atomic_energies_input, dict):
        atomic_energies_dict = atomic_energies_input
        logging.info(f"Use Atomic Energies that are provided: {atomic_energies_dict}")
        atomic_energies = np.array(
            [atomic_energies_dict.get(z, 0.0) for z in range(num_species)]
        )
    else:
        raise ValueError(
            f"The requested strategy for atomic energies "
            f"handling '{atomic_energies_input}' is not supported."
        )

    if len(z_table.zs) > num_species:
        raise ValueError(
            f"len(z_table.zs)={len(z_table.zs)} > num_species={num_species}"
        )

    return atomic_energies
