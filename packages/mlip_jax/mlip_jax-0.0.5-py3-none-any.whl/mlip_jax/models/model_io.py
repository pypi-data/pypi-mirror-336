import json
import os
from copy import deepcopy
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any
from zipfile import ZipFile

import numpy as np

from mlip_jax.data.dataset_info import DatasetInfo
from mlip_jax.models.type_aliases import ModelParameters
from mlip_jax.utils.dict_flatten import flatten_dict, unflatten_dict

PARAMETER_MODULE_DELIMITER = "#"
MODEL_FACTORY_KWARGS_FILENAME = "model_factory_kwargs.json"
MODEL_PARAMETERS_FILENAME = "params.npz"


def save_model_to_zip(
    save_path: str | os.PathLike,
    params: ModelParameters,
    model_factory_kwargs: dict[str, Any],
) -> None:
    """Saves model to a zip archive in a lightweight format to be easily loaded back
    for inference later.

    Args:
        save_path: The target path to the zip archive. Should have extension ".zip".
        params: The model parameters to save.
        model_factory_kwargs: The kwargs as a dictionary that were passed to the model
                      factory function. It defines the model configuration.
                      For example, for MACE, it would be the kwargs passed to
                      this function:
                      :meth:`~mlip_jax.models.mace.create_mace_force_field`
    """
    if "dataset_info" not in model_factory_kwargs:
        raise ValueError("Dataset info must be in model factory kwargs!")

    model_factory_kwargs_copy = deepcopy(model_factory_kwargs)
    dataset_info = model_factory_kwargs_copy.pop("dataset_info")

    model_factory_kwargs_processed = {
        "dataset_info": json.loads(dataset_info.model_dump_json()),
        **model_factory_kwargs_copy,
    }

    params_flattened = {
        PARAMETER_MODULE_DELIMITER.join(key_as_tuple): array
        for key_as_tuple, array in flatten_dict(params).items()
    }

    with TemporaryDirectory() as tmpdir:
        kwargs_path = Path(tmpdir) / MODEL_FACTORY_KWARGS_FILENAME
        params_path = Path(tmpdir) / MODEL_PARAMETERS_FILENAME

        with open(kwargs_path, "w") as json_file:
            json.dump(model_factory_kwargs_processed, json_file)

        np.savez(params_path, **params_flattened)

        with ZipFile(save_path, "w") as zip_object:
            zip_object.write(kwargs_path, os.path.basename(kwargs_path))
            zip_object.write(params_path, os.path.basename(params_path))


def load_model_from_zip(
    load_path: str | os.PathLike,
) -> tuple[ModelParameters, dict[str, Any]]:
    """Loads a model from a zip archive.

    Args:
        load_path: The path to the zip archive to load.

    Returns:
        The loaded model parameters and a dictionary of kwargs that can be passed to
        a model factory function like, for example,
        :meth:`~mlip_jax.models.mace.create_mace_force_field` for MACE.
    """
    with ZipFile(load_path, "r") as zip_object:
        with zip_object.open(MODEL_FACTORY_KWARGS_FILENAME, "r") as kwargs_file:
            kwargs_raw = json.load(kwargs_file)
        with zip_object.open(MODEL_PARAMETERS_FILENAME, "r") as params_file:
            params_raw = np.load(params_file)
            params = unflatten_dict(
                {
                    tuple(key.split(PARAMETER_MODULE_DELIMITER)): params_raw[key]
                    for key in params_raw.files
                }
            )

    dataset_info = DatasetInfo(**kwargs_raw.pop("dataset_info"))
    model_factory_kwargs = {"dataset_info": dataset_info, **kwargs_raw}

    return params, model_factory_kwargs
