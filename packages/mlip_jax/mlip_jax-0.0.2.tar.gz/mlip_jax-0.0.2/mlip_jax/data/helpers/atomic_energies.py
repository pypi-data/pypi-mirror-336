import logging

import jraph
import numpy as np


def compute_average_e0s_from_graphs(
    graphs: list[jraph.GraphsTuple],
) -> dict[int, float]:
    """Compute average energy contribution of each element by least squares.

    Args:
        graphs: The graphs for which to compute the average energy
                contribution of each element

    Returns:
        The atomic energies dictionary which is the mapping of atomic species to
        the average energy contribution of each element.
    """
    num_graphs = len(graphs)
    unique_species = sorted(set(np.concatenate([g.nodes.species for g in graphs])))
    num_unique_species = len(unique_species)

    species_count = np.zeros((num_graphs, num_unique_species))
    energies = np.zeros(num_graphs)

    for i in range(num_graphs):
        energies[i] = graphs[i].globals.energy
        for j, species_number in enumerate(unique_species):
            species_count[i, j] = np.count_nonzero(
                graphs[i].nodes.species == species_number
            )

    try:
        e0s = np.linalg.lstsq(species_count, energies, rcond=1e-8)[0]
        atomic_energies = {}
        for i, species_number in enumerate(unique_species):
            atomic_energies[species_number] = e0s[i]

    except np.linalg.LinAlgError:
        logging.warning(
            "Failed to compute E0s using "
            "least squares regression, using the 0.0 for all atoms."
        )
        atomic_energies = dict.fromkeys(unique_species, 0.0)

    return atomic_energies
