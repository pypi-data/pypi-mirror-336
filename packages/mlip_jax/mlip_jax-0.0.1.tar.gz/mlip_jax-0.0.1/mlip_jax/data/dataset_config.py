from pathlib import Path
from typing import Optional

import pydantic
from omegaconf import DictConfig, ListConfig
from pydantic import Field, field_validator
from typing_extensions import Annotated

PositiveInt = Annotated[int, pydantic.Field(gt=0)]
PositiveFloat = Annotated[float, pydantic.Field(gt=0)]


class DataLoaderConfig(pydantic.BaseModel):
    """Pydantic-based config related to dataset preprocessing.

    Attributes:
        loader_type: Type of the data loader (hdf5, extxyz, ...) to know which one
                     to use for this specific dataset.
        train_dataset_paths: Path to where the training set is located.
                            Cannot be empty.
                            Will be converted to a list after validation.
        valid_dataset_paths: Path to where the validation set is located.
                            This can be empty.
                            Will be converted to a list after validation.
        test_dataset_paths: Path to where the test set is located.
                            This can be empty.
                            Will be converted to a list after validation.
        train_num_to_load: Number of training set data points to load from the given
                           dataset. By default, this is ``None`` which means all the
                           data points are loaded.
                           If multiple dataset paths are given, then this limit will
                           apply to each path separately, not in total.
        valid_num_to_load: Number of validation set data points to load from the given
                           dataset. By default, this is ``None`` which means all the
                           data points are loaded.
                           If multiple dataset paths are given, then this limit will
                           apply to each path separately, not in total.
        test_num_to_load: Number of test set data points to load from the given
                           dataset. By default, this is ``None`` which means all the
                           data points are loaded.
                           If multiple dataset paths are given, then this limit will
                           apply to each path separately, not in total.
    """

    loader_type: str = Field(alias="type", default="extxyz")
    train_dataset_paths: list[str | Path] = Field(min_length=1)
    valid_dataset_paths: list[str | Path]
    test_dataset_paths: list[str | Path]

    train_num_to_load: Optional[PositiveInt] = None
    valid_num_to_load: Optional[PositiveInt] = None
    test_num_to_load: Optional[PositiveInt] = None

    @field_validator(
        "train_dataset_paths",
        "valid_dataset_paths",
        "test_dataset_paths",
        mode="before",
    )
    @classmethod
    def convert_to_list(
        cls, value: str | Path | list[str | Path] | ListConfig | None
    ) -> list[str | Path]:
        """Support single element input for a list field, by converting it to a list
        internally to simplify usage."""
        if value is None:
            return []
        if isinstance(value, (str, Path)):
            return [value]
        if isinstance(value, list):
            return value
        if isinstance(value, ListConfig):
            return list(value)
        raise ValueError(
            f"*_dataset_paths must be a string, Path, or a list of them, "
            f"but was {type(value)} - {value}"
        )


class DatasetConfig(pydantic.BaseModel):
    """Pydantic-based config related to dataset preprocessing.

    Attributes:
        data_loaders: List of ``DataLoaderConfig``.
        graph_cutoff_angstrom: Graph cutoff distance in Angstrom to apply when
                               creating the graphs.
        max_n_node: This value will be multiplied with the batch size to determine the
                    maximum number of nodes we allow in a batch.
                    Note that a batch will always contain max_n_node * batch_size
                    nodes, as the remaining ones are filled up with dummy nodes.
        max_n_edge: This value will be multiplied with the batch size to determine the
                    maximum number of edges we allow in a batch.
                    Note that a batch will always contain max_n_edge * batch_size
                    edges, as the remaining ones are filled up with dummy edges.
        batch_size: The number of graphs in a batch. Will be filled up with dummy graphs
                    if either the maximum number of nodes or edges are reached before
                    the number of graphs is reached.
        num_batch_prefetch: Number of batched graphs to prefetch while iterating
                            over batches. Default is 1.
        batch_prefetch_num_devices: Number of threads to use for prefetching.
                                    Default is 1.
        use_formation_energies: Whether the energies in the dataset should already be
                                transformed to subtract the average atomic energies.
                                Default is ``False``. Make sure that if you set this
                                to ``True``, the models assume ``"zero"`` atomic
                                energies as can be set in the model hyperparameters.
        avg_num_neighbors: The pre-computed average number of neighbors.
        avg_r_min_angstrom: The pre-computed average minimum distance between nodes.

    """

    data_loaders: list[DataLoaderConfig] = Field(min_length=1)
    graph_cutoff_angstrom: PositiveFloat
    max_n_node: Optional[PositiveInt]
    max_n_edge: Optional[PositiveInt]
    batch_size: PositiveInt

    num_batch_prefetch: PositiveInt = 1
    batch_prefetch_num_devices: PositiveInt = 1

    use_formation_energies: bool = False
    avg_num_neighbors: Optional[float] = None
    avg_r_min_angstrom: Optional[float] = None

    @field_validator(
        "data_loaders",
        mode="before",
    )
    @classmethod
    def convert_to_list(cls, value: DictConfig | ListConfig | None) -> list[str | Path]:
        """Support single element input for a list field, by converting it to a list
        internally to simplify usage."""
        if value is None:
            return []
        if isinstance(value, DictConfig):
            return [value]
        if isinstance(value, ListConfig):
            return list(value)
        if isinstance(value, list):
            return value
        if isinstance(value, DataLoaderConfig):
            return [value]
        raise ValueError(
            f"data_loaders must be a dict or a list of dicts, "
            f"but was {type(value)} - {value}"
        )

    @property
    def data_loader(self) -> DataLoaderConfig:
        """Can only be used as a convenience property if only one data_loader."""
        if len(self.data_loaders) == 1:
            return self.data_loaders[0]
        raise ValueError(
            f"Must have only one data loader to access without indexing! "
            f"Length={len(self.data_loaders)}"
        )
