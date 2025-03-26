import abc
import os
from typing import Callable, Optional, TypeAlias

from mlip_jax.data.data_loaders.type_aliases import (
    ChemicalSystems,
    ChemicalSystemsBySplit,
)
from mlip_jax.data.data_loaders.utils import (
    filter_systems_with_unseen_atoms_and_assign_atomic_species,
)
from mlip_jax.data.dataset_config import DatasetConfig

Source: TypeAlias = str | os.PathLike
Target: TypeAlias = str | os.PathLike


class DataLoader(abc.ABC):
    """Abstract base class for loading data into the internal format of lists
    of ``ChemicalSystem`` objects, one list for training data, one for validation, and
    one for test data."""

    def __init__(
        self, data_download_fun: Optional[Callable[[Source, Target], None]] = None
    ):
        """Constructor.

        Args:
            data_download_fun: A function to download data from an external remote
                               system. If ``None`` (default), then this class assumes
                               file paths are local. This function must take two paths
                               as input, source and target, and download the data at
                               source into the target location.
        """
        self.data_download_fun = data_download_fun

    @abc.abstractmethod
    def load(
        self,
        dataset_config: DatasetConfig,
        postprocess_fun: Optional[
            Callable[
                [ChemicalSystems, ChemicalSystems, ChemicalSystems],
                ChemicalSystemsBySplit,
            ]
        ] = filter_systems_with_unseen_atoms_and_assign_atomic_species,
    ) -> ChemicalSystemsBySplit:
        """Loads the dataset into its internal format.

        Args:
            dataset_config: The dataset config specifying all required information,
                            for example, the dataset location.
            postprocess_fun: Function to call to postprocess the loaded dataset
                            before returning it. Accepts train, validation and test
                            systems (``list[ChemicalSystems]``), runs some
                            postprocessing (filtering for example) and
                            returns the postprocessed train, validation and test
                            systems.
                            If ``postprocess_fun`` is ``None`` then no postprocessing
                            will be done. By default, it will run
                            :meth:`~mlip_jax.data.data_loaders.utils.assign_atomic_species_and_filter_systems_with_unseen_atoms`
                            which assigns atomic species on ``ChemicalSystem`` objects
                            and filters out systems from the validation
                            and test sets that contain chemical elements that
                            are not present in the train systems.
        Returns:
            A tuple of loaded training, validation and test datasets (in this order).
            The internal format is a list of ``ChemicalSystem`` objects.
        """
        pass
