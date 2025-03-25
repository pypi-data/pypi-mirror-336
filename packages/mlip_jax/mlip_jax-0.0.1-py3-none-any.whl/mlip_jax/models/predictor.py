from typing import TypeAlias

import e3nn_jax as e3nn
import flax.linen as nn
import jax
import jax.numpy as jnp
import jraph
import numpy as np

from mlip_jax.data.helpers.edge_vectors import get_edge_relative_vectors

RelativeEdgeVectors: TypeAlias = np.ndarray
AtomicSpecies: TypeAlias = np.ndarray
Senders: TypeAlias = np.ndarray
Receivers: TypeAlias = np.ndarray
NodeEnergies: TypeAlias = np.ndarray


class ForceFieldPredictor(nn.Module):
    """Flax module for a force field predictor.

    The apply function of this predictor returns the force field function used basically
    everywhere in the rest of the code base. This module is initialized from an
    already constructed MLIP model network module and a boolean whether to predict
    stress properties.

    Attributes:
        mlip_network: The MLIP network.
        predict_stress: Whether to predict stress properties. If false, only energies
                        and forces are computed.
    """

    mlip_network: nn.Module
    predict_stress: bool

    def __call__(self, graph: jraph.GraphsTuple) -> dict[str, np.ndarray]:
        """Returns a dictionary of properties based on an input graph.

        Args:
            graph: The input graph.

        Returns:
            The properties in a dictionary with keys that may include "energy",
            "forces", "stress", "stress_cell", "stress_forces", and "pressure".
            Only the first two exist if ``predict_stress=False`` is set for this module.
        """
        graph_energies, minus_forces, pseudo_stress = (
            self._compute_graph_energies_and_grad_wrt_positions(graph)
        )

        result = {
            "energy": graph_energies,  # [n_graphs,] energy per cell [eV]
            "forces": -minus_forces,  # [n_nodes, 3] forces on each atom [eV / A]
        }

        if not self.predict_stress:
            return result

        stress_results = self._compute_stress_results(
            graph, pseudo_stress, minus_forces
        )
        result.update(stress_results)
        return result

    def _compute_graph_energies_and_grad_wrt_positions(
        self, graph: jraph.GraphsTuple
    ) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        (gradients, pseudo_stress), node_energies = jax.grad(
            self._compute_energy, (0, 1), has_aux=True
        )(graph.nodes.positions, graph.globals.cell, graph)

        graph_energies = e3nn.scatter_sum(
            node_energies, nel=graph.n_node
        )  # [ n_graphs,]

        return graph_energies, gradients, pseudo_stress

    @staticmethod
    def _compute_stress_results(
        graph: jraph.GraphsTuple,
        pseudo_stress: np.ndarray,
        minus_forces: np.ndarray,
    ) -> dict[str, np.ndarray]:
        assert (
            graph.edges.shifts is not None
        ), "without shifts, the computed pseudo_stress is incorrect"

        det = jnp.linalg.det(graph.globals.cell)[:, None, None]  # [n_graphs, 1, 1]
        det = jnp.where(det > 0.0, det, 1.0)  # dummy graphs have det = 0

        stress_cell = (
            jnp.transpose(pseudo_stress, (0, 2, 1)) @ graph.globals.cell
        )  # [n_graphs, 3, 3]
        stress_forces = e3nn.scatter_sum(
            jnp.einsum("iu,iv->iuv", minus_forces, graph.nodes.positions),
            nel=graph.n_node,
        )  # [n_graphs, 3, 3]
        viriel = stress_cell + stress_forces  # NOTE: sign suggested by Ilyes Batatia
        stress = -1.0 / det * viriel  # NOTE: sign suggested by Ilyes Batatia

        # TODO(mario): fix this
        # make it traceless? because it seems that our formula is not
        # valid for the trace
        pressure = jnp.trace(stress, axis1=1, axis2=2)  # [n_graphs,]
        # stress = stress - p[:, None, None] / 3.0 * jnp.eye(3)

        return {
            "stress": stress,  # [n_graphs, 3, 3] stress tensor [eV / A^3]
            "stress_cell": (
                -1.0 / det * stress_cell
            ),  # [n_graphs, 3, 3] stress tensor [eV / A^3]
            "stress_forces": (
                -1.0 / det * stress_forces
            ),  # [n_graphs, 3, 3] stress tensor [eV / A^3]
            "pressure": pressure,  # [n_graphs,] pressure [eV / A^3]
        }

    def _compute_energy(
        self,
        positions: np.ndarray,
        cell: np.ndarray,
        graph: jraph.GraphsTuple,
    ) -> tuple[float, np.ndarray]:
        if graph.edges.shifts is None:
            assert graph.edges.displ_fun is not None
            vectors = graph.edges.displ_fun(
                positions[graph.receivers], positions[graph.senders]
            )
        else:
            vectors = get_edge_relative_vectors(
                positions=positions,
                senders=graph.senders,
                receivers=graph.receivers,
                shifts=graph.edges.shifts,
                cell=cell,
                n_edge=graph.n_edge,
            )

        node_energies = self.mlip_network(
            vectors, graph.nodes.species, graph.senders, graph.receivers
        )  # [n_nodes, ]
        node_energies = node_energies * jraph.get_node_padding_mask(graph)
        assert node_energies.shape == (len(positions),), (
            f"model output needs to be an array of shape "
            f"(n_nodes, ) but got {node_energies.shape}"
        )
        return jnp.sum(node_energies), node_energies
