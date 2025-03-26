import logging
import time
from typing import Optional

import jraph
import pydantic

from mlip_jax.data.helpers.atomic_energies import compute_average_e0s_from_graphs
from mlip_jax.data.helpers.atomic_number_table import AtomicNumberTable
from mlip_jax.data.helpers.neighbor_analysis import (
    compute_avg_min_neighbor_distance,
    compute_avg_num_neighbors,
)


class DatasetInfo(pydantic.BaseModel):
    """Pydantic dataclass holding information computed from the dataset that is
    (potentially) required by the models.

    Attributes:
        atomic_energies_map: A dictionary mapping the atomic numbers to the
                             computed average atomic energies for that element.
        avg_num_neighbors: The mean number of neighbors an atom has in the dataset.
        avg_r_min_angstrom: The mean minimum edge distance for a structure in the
                            dataset.
        cutoff_distance_angstrom: The graph cutoff distance that was
                                  used in the dataset in Angstrom.
        scaling_mean: The mean used for the rescaling of the dataset values, the
                      default being 0.0.
        scaling_stdev: The standard deviation used for the rescaling of the dataset
                       values, the default being 1.0.
    """

    atomic_energies_map: dict[int, float]
    avg_num_neighbors: float
    avg_r_min_angstrom: Optional[float]
    cutoff_distance_angstrom: float
    scaling_mean: float = 0.0
    scaling_stdev: float = 1.0

    def __str__(self):
        return (
            f"Atomic Energies: {self.atomic_energies_map}, "
            f"Avg. num. neighbors: {self.avg_num_neighbors:.2f}, "
            f"Avg. r_min: {self.avg_r_min_angstrom:.2f}, "
            f"Graph cutoff distance: {self.cutoff_distance_angstrom}"
        )


def compute_dataset_info_from_graphs(
    graphs: list[jraph.GraphsTuple],
    cutoff_distance_angstrom: float,
    z_table: AtomicNumberTable,
    avg_num_neighbors: Optional[float] = None,
    avg_r_min_angstrom: Optional[float] = None,
) -> DatasetInfo:
    """Computes the dataset info from graphs, typically training set graphs.

    Args:
        graphs: The graphs.
        cutoff_distance_angstrom: The graph distance cutoff in Angstrom to
                                  store in the dataset info.
        z_table: The atomic numbers table needed to produce the correct atomic energies
                 map keys.
        avg_num_neighbors: The optionally pre-computed average number of neighbors. If
                           provided, we skip recomputing this.
        avg_r_min_angstrom: The optionally pre-computed average miminum radius. If
                            provided, we skip recomputing this.


    Returns:
        The dataset info object populated with the computed data.
    """
    start_time = time.perf_counter()
    logging.info(
        "Starting to compute mandatory dataset statistics: this may take some time..."
    )
    if avg_num_neighbors is None:
        logging.info("Computing average number of neighbors...")
        avg_num_neighbors = compute_avg_num_neighbors(graphs)
        logging.info("Average number of neighbors: %.1f", avg_num_neighbors)
    if avg_r_min_angstrom is None:
        logging.info("Computing average min neighbor distance...")
        avg_r_min_angstrom = compute_avg_min_neighbor_distance(graphs)
        logging.info("Average min. node distance (Angstrom): %.1f", avg_r_min_angstrom)

    atomic_energies_map = {
        z_table.index_to_z(idx): energy
        for idx, energy in compute_average_e0s_from_graphs(graphs).items()
    }

    logging.info(
        "Computation of average atomic energies"
        " and dataset statistics completed in %.2f seconds.",
        time.perf_counter() - start_time,
    )

    return DatasetInfo(
        atomic_energies_map=atomic_energies_map,
        avg_num_neighbors=avg_num_neighbors,
        avg_r_min_angstrom=avg_r_min_angstrom,
        cutoff_distance_angstrom=cutoff_distance_angstrom,
        scaling_mean=0.0,
        scaling_stdev=1.0,
    )
