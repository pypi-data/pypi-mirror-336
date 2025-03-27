import logging
from math import ceil

import jax
import numpy as np
from ase import Atoms
from ase.calculators.calculator import Calculator, all_changes
from matscipy.neighbours import neighbour_list

from mlip_jax.data.helpers.dynamically_batch import dynamically_batch
from mlip_jax.simulation.simulation_engine import ModelParameters, ModelPredictorFun
from mlip_jax.simulation.utils import create_graph_from_atoms
from mlip_jax.utils.no_pbc_cell import get_no_pbc_cell


class MLIPForceFieldASECalculator(Calculator):
    """Atomic Simulation Environment (ASE) Calculator for JAX models.

    Implemented properties are energy and forces.
    """

    implemented_properties = [
        "energy",
        "forces",
    ]

    def __init__(
        self,
        atoms: Atoms,
        graph_cutoff_angstrom: float,
        allowed_atomic_numbers: set[int],
        edge_capacity_multiplier: float,
        model_apply_fun: ModelPredictorFun,
        model_params: ModelParameters,
        allow_nodes_to_change: bool = False,
        node_capacity_multiplier: float = 1.0,
    ) -> None:
        """Constructor.

        Args:
            atoms: Initial atomic structure.
            graph_cutoff_angstrom: Graph distance cutoff in Angstrom.
            allowed_atomic_numbers: The allowed atomic numbers for the model used in
                                    the simulation.
            edge_capacity_multiplier: Factor to multiply the number of edges by to
                                      obtain the edge capacity including padding.
            model_apply_fun: Function used to compute the predictions of a JAX model
                             using model parameters.
            model_params: The parameters of the MLIP model.
            allow_nodes_to_change: Whether the number or types of atoms/nodes may
                                   change for the same instance of this class. Defaults
                                   to ``False``.
            node_capacity_multiplier: Factor to multiply the number of nodes by to
                                      obtain the node capacity including padding.
                                      Defaults to 1.0.
        """
        self.atoms = atoms
        self.num_atoms = len(self.atoms)
        self.model_apply_fun = jax.jit(model_apply_fun)
        self.model_params = model_params
        self.graph_cutoff_angstrom = graph_cutoff_angstrom
        self.allowed_atomic_numbers = allowed_atomic_numbers
        self.edge_capacity_multiplier = edge_capacity_multiplier
        self.allow_nodes_to_change = allow_nodes_to_change
        self.node_capacity_multiplier = node_capacity_multiplier

        if np.any(atoms.pbc):
            senders, receivers, shifts = neighbour_list(
                quantities="ijS",
                cell=atoms.cell,
                pbc=atoms.pbc,
                positions=atoms.positions,
                cutoff=self.graph_cutoff_angstrom,
            )
        else:
            cell, cell_origin = get_no_pbc_cell(
                atoms.positions, self.graph_cutoff_angstrom
            )
            senders, receivers, shifts = neighbour_list(
                quantities="ijS",
                cell=cell,
                cell_origin=cell_origin,
                pbc=atoms.pbc,
                positions=atoms.positions,
                cutoff=self.graph_cutoff_angstrom,
            )

        num_edges = len(senders)

        _displacement_fun = None
        self.base_graph = create_graph_from_atoms(
            self.atoms,
            senders,
            receivers,
            _displacement_fun,
            self.allowed_atomic_numbers,
            cell=self.atoms.cell,
            shifts=shifts,
        )
        self.current_edge_capacity = ceil(self.edge_capacity_multiplier * num_edges)
        self.current_node_capacity = ceil(
            self.node_capacity_multiplier * len(self.atoms)
        )
        Calculator.__init__(self)

    def calculate(
        self,
        atoms: Atoms | None = None,
        properties: list[str] | None = None,
        system_changes: list[str] = all_changes,
    ) -> None:
        """Compute properties (``forces`` and/or ``energy``) and save them in
        ``self.results`` dictionary for ASE simulation.

        Args:
            atoms: Atomic structure. Defaults to ``None``.
            properties: List of what needs to be calculated.
                        Can be any combination of ``"energy"``, ``"forces"``.
                        Defaults to ``None``.
            system_changes: List of what has changed since last calculation.
                            Can be any combination of these six: ``"positions"``,
                            ``"numbers"``, ``"cell"``, ``"pbc"``, ``initial_charges``
                            and ``"initial_magmoms"``.
                            Defaults to ``ase.calculators.calculator.all_changes``.
        """
        if atoms is None:
            raise ValueError("Variable atoms should not be None.")
        if properties is None:
            properties = ["energy", "forces"]
        Calculator.calculate(self, atoms, properties, system_changes)

        # compute new edge info
        if np.any(atoms.pbc):
            senders, receivers, shifts = neighbour_list(
                quantities="ijS",
                cell=atoms.cell,
                pbc=atoms.pbc,
                positions=atoms.positions,
                cutoff=self.graph_cutoff_angstrom,
            )
        else:
            cell, cell_origin = get_no_pbc_cell(
                atoms.positions, self.graph_cutoff_angstrom
            )
            senders, receivers, shifts = neighbour_list(
                quantities="ijS",
                cell=cell,
                cell_origin=cell_origin,
                pbc=atoms.pbc,
                positions=atoms.positions,
                cutoff=self.graph_cutoff_angstrom,
            )

        # See if padding still enough
        num_edges = len(senders)
        if self.current_edge_capacity < num_edges:
            self.current_edge_capacity = ceil(self.edge_capacity_multiplier * num_edges)
            logging.info(
                "The edge capacity has been reset to %s.", self.current_edge_capacity
            )
        if self.allow_nodes_to_change and self.current_node_capacity < len(atoms):
            self.current_node_capacity = ceil(
                self.node_capacity_multiplier * len(atoms)
            )
            logging.info(
                "The edge capacity has been reset to %s.", self.current_edge_capacity
            )

        if self.allow_nodes_to_change:
            _displacement_fun = None
            graph = create_graph_from_atoms(
                atoms,
                senders,
                receivers,
                _displacement_fun,
                self.allowed_atomic_numbers,
                cell=atoms.cell,
                shifts=shifts,
            )
        else:
            graph = self.base_graph._replace(
                senders=senders,
                receivers=receivers,
                nodes=self.base_graph.nodes._replace(positions=atoms.positions),
                edges=self.base_graph.edges._replace(shifts=shifts),
                n_edge=np.array([len(senders)]),
            )

        # Batch with dummy
        batched_graph = next(
            dynamically_batch(
                [graph],
                n_node=self.current_node_capacity + 1,
                n_edge=self.current_edge_capacity + 1,
                n_graph=2,
            )
        )

        # Run predictions
        predictions = self.model_apply_fun(self.model_params, batched_graph)
        if "energy" in properties:
            self.results["energy"] = np.array(predictions["energy"][0])
        if "forces" in properties:
            self.results["forces"] = np.array(predictions["forces"])[: len(atoms), :]
