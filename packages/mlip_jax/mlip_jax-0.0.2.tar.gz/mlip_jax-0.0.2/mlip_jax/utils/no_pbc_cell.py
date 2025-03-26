import numpy as np


def get_no_pbc_cell(
    positions: np.ndarray, graph_cutoff: float
) -> tuple[np.ndarray, np.ndarray]:
    """Create a cell that contains all positions, with room to spare.

    Args:
        positions: A Nx3 array of the positions of the atoms in Angstrom.
        graph_cutoff: The maximum distance for an edge to be computed between two atoms
                      in Angstrom.

    Returns:
        A tuple of the cell, as an array of size 3,
        and a cell origin, as an array of size 3.
    """
    rmax = np.max(positions, axis=0)
    rmin = np.min(positions, axis=0)
    return np.diag(graph_cutoff * 4 + (rmax - rmin)), rmin - graph_cutoff * 2
