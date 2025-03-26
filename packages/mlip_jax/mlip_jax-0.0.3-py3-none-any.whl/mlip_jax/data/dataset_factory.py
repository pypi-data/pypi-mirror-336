import functools
import logging
from typing import Optional, TypeAlias

import jax
import jraph
import numpy as np
from tqdm_loggable.auto import tqdm

from mlip_jax.data.chemical_system import ChemicalSystem
from mlip_jax.data.data_loaders.data_loader import DataLoader
from mlip_jax.data.dataset_config import DatasetConfig
from mlip_jax.data.dataset_info import DatasetInfo, compute_dataset_info_from_graphs
from mlip_jax.data.helpers.atomic_number_table import AtomicNumberTable
from mlip_jax.data.helpers.data_prefetching import (
    ParallelGraphDataManager,
    PrefetchIterator,
    create_prefetch_iterator,
)
from mlip_jax.data.helpers.graph_creation import create_graph_from_chemical_system
from mlip_jax.data.helpers.graph_data_manager import GraphDataManager

GraphDataManagersOrPrefetchedIterators: TypeAlias = (
    tuple[GraphDataManager, GraphDataManager, GraphDataManager]
    | tuple[PrefetchIterator, PrefetchIterator, PrefetchIterator]
)


class DatasetsHaveNotBeenProcessedError(Exception):
    """Exception to be raised if dataset info is not available yet."""


class DevicesNotProvidedForPrefetchingError(Exception):
    """Exception to be raised if devices are not provided
    even though prefetching of data was requested.
    """


class DatasetFactory:
    """Main class handling the preprocessing/preparation of the dataset.

    The key idea is that a user provides a data loader class that loads a dataset into
    :class:`~mlip_jax.data.chemical_system.ChemicalSystem` dataclasses and then this
    class converts these further to jraph graphs and the dataset info dataclass.
    """

    def __init__(self, data_loader: DataLoader, dataset_config: DatasetConfig):
        """Constructor.

        Args:
            data_loader: The data loder that loads a dataset into
                         :class:`~mlip_jax.data.chemical_system.ChemicalSystem`
                         dataclasses
            dataset_config: The pydantic config.
        """
        self._data_loader = data_loader
        self._config = dataset_config
        self._dataset_info: Optional[DatasetInfo] = None
        self._data_managers: Optional[dict[str, Optional[GraphDataManager]]] = None

    def get_datasets(
        self, prefetch: bool = False, devices: Optional[list[jax.Device]] = None
    ) -> GraphDataManagersOrPrefetchedIterators:
        """Returns the training, validation, and test datasets.

        Args:
            prefetch: Whether to run the data prefetching and return PrefetchIterators.
            devices: Devices for parallel prefetching. Must be given if prefetch=True.

        Returns:
            A tuple of training, validation, and test datasets. If prefetch=False,
            these are of type GraphDataManager, otherwise of type PrefetchIterator.
        """
        if self._data_managers is None:
            raise DatasetsHaveNotBeenProcessedError(
                "Datasets are not available yet. Run prepare_dataset_splits() first."
            )

        if prefetch:
            if devices is None:
                raise DevicesNotProvidedForPrefetchingError(
                    "Please provide the devices argument when prefetch=True."
                )
            return self._get_prefetched_iterators(devices)
        return (
            self._data_managers["train"],
            self._data_managers["valid"],
            self._data_managers["test"],
        )

    def prepare_datasets(self) -> None:
        """Prepares the datasets.

        This includes loading it into ChemicalSystem objects via the data loader,
        and then producing the graph data managers and the dataset info object.
        """
        train_systems, valid_systems, test_systems = self._data_loader.load(
            self._config
        )
        z_table = self._construct_z_table(train_systems)

        train_graph_manager, valid_graph_manager, test_graph_manager = (
            self._create_graph_managers_from_chemical_systems(
                train_systems, valid_systems, test_systems
            )
        )

        logging.info(
            "Number of graphs in training set: %s", len(train_graph_manager.graphs)
        )
        logging.info(
            "Number of graphs in validation set: %s", len(valid_graph_manager.graphs)
        )
        logging.info("Number of graphs in test set: %s", len(test_graph_manager.graphs))

        self._dataset_info = compute_dataset_info_from_graphs(
            train_graph_manager.graphs,
            self._config.graph_cutoff_angstrom,
            z_table,
            self._config.avg_num_neighbors,
            self._config.avg_r_min_angstrom,
        )

        self._data_managers = {
            "train": train_graph_manager,
            "valid": valid_graph_manager,
            "test": test_graph_manager,
        }

        if self._config.use_formation_energies:
            self._convert_energies_to_formation_energies(z_table)

    @property
    def dataset_info(self) -> DatasetInfo:
        """Getter for the dataset info.

        Will raise exception if dataset info not available yet.
        """
        if self._dataset_info is None:
            raise DatasetsHaveNotBeenProcessedError(
                "Dataset info not available yet. Run prepare_dataset_splits() first."
            )
        return self._dataset_info

    @staticmethod
    def _filter_out_bad_graphs(
        graphs: list[jraph.GraphsTuple],
    ) -> list[jraph.GraphsTuple]:
        """Filter out graphs. This function implements the following subfunctions:

        1. Remove empty graphs (graphs with no edges).
        """

        def filter_empty_graphs(
            graphs: list[jraph.GraphsTuple],
        ) -> list[jraph.GraphsTuple]:
            filtered_graphs, num_discarded_graphs = [], 0
            for graph in graphs:
                if graph.n_edge.sum() == 0:
                    num_discarded_graphs += 1
                else:
                    filtered_graphs.append(graph)
            logging.warning(
                "Discarded %s empty graphs due to having no edges", num_discarded_graphs
            )
            return filtered_graphs

        graphs = filter_empty_graphs(graphs)
        return graphs

    def _create_graph_managers_from_chemical_systems(
        self,
        train_systems: list[ChemicalSystem],
        valid_systems: list[ChemicalSystem],
        test_systems: list[ChemicalSystem],
    ) -> tuple[GraphDataManager, GraphDataManager, GraphDataManager]:
        _cfg = self._config
        graph_data_managers = {}

        # Train graphs will be returned as None if not calculated below
        max_n_node, max_n_edge, train_graphs = (
            self._determine_autofill_batch_limitations(train_systems)
        )

        for key, systems, should_shuffle in [
            ("train", train_systems, True),
            ("valid", valid_systems, False),
            ("test", test_systems, False),
        ]:
            if key == "train" and train_graphs is not None:
                graphs = train_graphs  # here: train graphs have been computed above
            else:
                graphs = [
                    create_graph_from_chemical_system(
                        system, _cfg.graph_cutoff_angstrom
                    )
                    for system in tqdm(systems, desc=f"{key} graph creation")
                ]
                graphs = self._filter_out_bad_graphs(graphs)

            graph_data_manager = GraphDataManager(
                graphs=graphs,
                max_n_node=max_n_node,
                max_n_edge=max_n_edge,
                batch_size=_cfg.batch_size,
                should_shuffle=should_shuffle,
            )
            graph_data_managers[key] = graph_data_manager

        return (
            graph_data_managers["train"],
            graph_data_managers["valid"],
            graph_data_managers["test"],
        )

    @staticmethod
    def _construct_z_table(train_systems: list[ChemicalSystem]) -> AtomicNumberTable:
        return AtomicNumberTable(
            sorted(
                set(np.concatenate([system.atomic_numbers for system in train_systems]))
            )
        )

    def _get_prefetched_iterators(
        self, devices: list[jax.Device]
    ) -> tuple[PrefetchIterator, PrefetchIterator, PrefetchIterator]:
        _cfg = self._config
        num_devices = len(devices)

        device_shard_fn = functools.partial(
            jax.tree_map,
            lambda x: jax.device_put_sharded(list(x), devices),
        )

        prefetched_iterators = {}

        for key, data_manager in self._data_managers.items():
            parallel_manager = ParallelGraphDataManager(data_manager, num_devices)
            prefetched_iterator = create_prefetch_iterator(
                create_prefetch_iterator(
                    parallel_manager,
                    prefetch_count=_cfg.num_batch_prefetch,
                ),
                prefetch_count=_cfg.batch_prefetch_num_devices,
                preprocess_fn=device_shard_fn,
            )
            prefetched_iterators[key] = prefetched_iterator

        return (
            prefetched_iterators["train"],
            prefetched_iterators["valid"],
            prefetched_iterators["test"],
        )

    def _determine_autofill_batch_limitations(
        self, train_systems: list[ChemicalSystem]
    ) -> tuple[int, int, Optional[list[jraph.GraphsTuple]]]:
        _cfg = self._config

        # Autofill max_n_node and max_n_edge if they are set to None
        if _cfg.max_n_node is None:
            max_n_node, max_num_atoms = self._get_median_and_max_num_atoms(
                train_systems
            )
            if _cfg.batch_size * max_n_node < max_num_atoms:
                logging.info("Largest graph does not fit into batch -> resizing it.")
                max_n_node = int(np.ceil(max_num_atoms / _cfg.batch_size))

            logging.info(
                "The batching parameter max_n_node has been computed to be %s.",
                max_n_node,
            )
        else:
            max_n_node = _cfg.max_n_node

        if _cfg.max_n_edge is None:
            train_graphs, num_discarded_graphs = [], 0
            for system in tqdm(train_systems, desc="Graph creation"):
                graph = create_graph_from_chemical_system(
                    system, _cfg.graph_cutoff_angstrom
                )
                if graph.n_edge.sum() == 0:
                    num_discarded_graphs += 1
                else:
                    train_graphs.append(graph)
            logging.info(
                "Discarded %s empty graphs due to having no edges", num_discarded_graphs
            )
            median_n_nei, max_total_edges = (
                self._get_median_num_neighbors_and_max_total_edges(train_graphs)
            )
            max_n_edge = median_n_nei * max_n_node // 2

            if max_n_edge * _cfg.batch_size * 2 < max_total_edges:
                logging.info("Largest graph does not fit into batch -> resizing it.")
                max_n_edge = int(np.ceil(max_total_edges / (2 * _cfg.batch_size)))

            logging.info(
                "The batching parameter max_n_edge has been computed to be %s.",
                max_n_edge,
            )
        else:
            train_graphs = None
            max_n_edge = _cfg.max_n_edge

        return max_n_node, max_n_edge, train_graphs

    @staticmethod
    def _get_median_and_max_num_atoms(
        chemical_systems: list[ChemicalSystem],
    ) -> tuple[int, int]:
        num_atoms = [system.atomic_numbers.shape[0] for system in chemical_systems]
        return int(np.ceil(np.median(num_atoms))), max(num_atoms)

    @staticmethod
    def _get_median_num_neighbors_and_max_total_edges(
        graphs: list[jraph.GraphsTuple],
    ) -> tuple[int, int]:
        num_neighbors = []
        current_max = 0

        for graph in graphs:
            _, counts = np.unique(graph.receivers, return_counts=True)
            current_max = max(current_max, counts.sum())
            num_neighbors.append(counts)

        median = int(np.ceil(np.median(np.concatenate(num_neighbors)).item()))
        return median, current_max

    def _convert_energies_to_formation_energies(
        self, z_table: AtomicNumberTable
    ) -> None:
        for data_manager in self._data_managers.values():
            data_manager.graphs = [
                self._convert_energy_to_formation_energy(graph, z_table)
                for graph in data_manager.graphs
            ]

    def _convert_energy_to_formation_energy(
        self, graph: jraph.GraphsTuple, z_table: AtomicNumberTable
    ) -> jraph.GraphsTuple:
        sum_atomic_energies = sum(
            self.dataset_info.atomic_energies_map.get(z_table.index_to_z(key), 0.0)
            for key in graph.nodes.species
        )
        formation_energy = graph.globals.energy - np.array(sum_atomic_energies)
        return graph._replace(globals=graph.globals._replace(energy=formation_energy))
