from typing import Callable, Optional

from mlip_jax.data.data_loaders.data_loader import DataLoader, Source, Target
from mlip_jax.data.data_loaders.type_aliases import (
    ChemicalSystems,
    ChemicalSystemsBySplit,
)
from mlip_jax.data.data_loaders.utils import (
    filter_systems_with_unseen_atoms_and_assign_atomic_species,
)
from mlip_jax.data.dataset_config import DatasetConfig


class CombinedDataLoader(DataLoader):
    """Implementation of a data loader that combines other data loaders."""

    def __init__(
        self,
        data_download_fun: Optional[Callable[[Source, Target], None]] = None,
        data_loaders_by_type: dict[str, DataLoader] = None,
    ):
        """Constructor.

        Args:
            data_download_fun: A function to download data from an external remote
                   system. If ``None`` (default), then this class assumes
                   file paths are local. This function must take two paths
                   as input, source and target, and download the data at
                   source into the target location.
            data_loaders_by_type: A dictionary of instantiated data loaders that are
                available to be used for combining. The keys are the data loader
                types that are specified in the data loader's config that is part of
                the dataset factory's config.
        """
        super().__init__(data_download_fun)
        self.data_loaders_by_type = data_loaders_by_type

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

        _cfg = dataset_config
        train_systems, valid_systems, test_systems = [], [], []
        for data_loader_conf in _cfg.data_loaders:
            if data_loader_conf.loader_type not in self.data_loaders_by_type:
                raise ValueError(
                    f"Data loader of type {data_loader_conf.loader_type} "
                    f"is not available in data_loaders_by_type!"
                )
            data_loader = self.data_loaders_by_type[data_loader_conf.loader_type]
            # give a modified copy with only this one data_loader to make it easier
            # to use regular data loaders.
            single_conf = _cfg.model_copy(
                update={"data_loaders": [data_loader_conf]},
                deep=True,
            )
            # skip postprocess since will do it afterwards, after
            # having combined all the systems from different dataloaders
            train_sys, valid_sys, test_sys = data_loader.load(
                single_conf, postprocess_fun=None
            )
            train_systems += train_sys
            valid_systems += valid_sys
            test_systems += test_sys

        if postprocess_fun is not None:
            train_systems, valid_systems, test_systems = postprocess_fun(
                train_systems, valid_systems, test_systems
            )

        return train_systems, valid_systems, test_systems
