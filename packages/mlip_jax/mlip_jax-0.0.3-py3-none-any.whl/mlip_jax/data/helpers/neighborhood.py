from typing import Optional

import matscipy.neighbours
import numpy as np


def get_neighborhood(
    positions: np.ndarray,  # [num_positions, 3]
    cutoff: float,
    pbc: Optional[tuple[bool, bool, bool]] = None,
    cell: Optional[np.ndarray] = None,  # [3, 3]
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Computes the edge information for a given set of positions, including senders,
    receivers, and shift vectors.

    If ``pbc`` is ``None`` or ``(False, False, False)``, then the shifts will be
    returned as zero.
    This is the default behavior. The cell is None as default and as a result, matscipy
    will compute the minimal cell size needed to fit the whole system. See matscipy's
    documentation for more information.

    Args:
        positions: The position matrix.
        cutoff: The distance cutoff for the edges in Angstrom.
        pbc: A tuple of bools representing if periodic boundary conditions exist in
             any of the spatial dimensions. Default is None, which means False in every
             direction.
        cell: The unit cell of the system given as a 3x3 matrix or as None (default),
              which means that matscipy will compute the minimal cell size needed to
              fit the whole system.

    Returns:
        A tuple of **senders** (starting indexes of atoms for each edge), **receivers**
        (ending indexes of atoms for each edge), and **shifts** (the shift vectors, see
        matscipy's documentation for more information. If PBCs are false,
        then we return shifts of zero).

    """
    if pbc is None:
        pbc = (False, False, False)

    if np.all(cell == 0.0):
        cell = None

    assert len(pbc) == 3 and all(isinstance(i, (bool, np.bool_)) for i in pbc)
    assert cell is None or cell.shape == (3, 3)

    # Note (mario): I swapped senders and receivers here
    # j = senders, i = receivers instead of the other way around
    # such that the receivers are always in the central cell.
    # This is important to propagate message passing towards
    # the center which can be useful in some cases.
    receivers, senders, senders_unit_shifts = matscipy.neighbours.neighbour_list(
        quantities="ijS",
        pbc=pbc,
        cell=cell,
        positions=positions,
        cutoff=cutoff,
    )

    # If we are not having PBCs, then use shifts of zero
    shifts = senders_unit_shifts if any(pbc) else np.array([[0] * 3] * len(senders))

    # From the docs: With the shift vector S, the distances D between atoms
    # can be computed from
    # D = positions[j]-positions[i]+S.dot(cell)
    # Note (mario): this is done in the function get_edge_relative_vectors
    return senders, receivers, shifts
