import logging
from typing import Optional, Union

import jax

from mlip_jax.data.dataset_info import DatasetInfo
from mlip_jax.data.helpers.dummy_init_graph import get_dummy_graph_for_model_init
from mlip_jax.models.atomic_energies import get_atomic_energies
from mlip_jax.models.predictor import ForceFieldPredictor
from mlip_jax.models.type_aliases import ModelParameters, ModelPredictorFun
from mlip_jax.models.visnet.models import Visnet


def create_visnet_force_field(
    dataset_info: DatasetInfo,
    initialize_seed: int = 42,
    num_layers: int = 4,
    num_channels: int = 256,
    l_max: int = 2,
    num_heads: int = 8,
    num_rbf: int = 32,
    trainable_rbf: bool = False,
    activation: str = "silu",
    attn_activation: str = "silu",
    vecnorm_type: str = None,
    predict_stress: bool = False,
    atomic_energies: Optional[Union[str, dict[int, float]]] = None,
    learnable_atomic_energies: bool = False,
    num_species: Optional[int] = None,
    return_uninitialized_module: bool = False,
) -> tuple[ModelPredictorFun, ModelParameters] | ForceFieldPredictor:
    """For the ViSNet model, by default, this creates the force field model predictor
    function and initial parameters for it. Alternatively, one can also get the
    uninitialized module returned directly by setting ``return_uninitialized_module``
    to ``True``.

    Args:
        dataset_info: The dataset info object obtained from the data preprocessing step.
        initialize_seed: A random seed for weight initialization. By default,
                         this is 42. Has no effect
                         if ``return_uninitialized_module`` is set to ``True``.
        num_layers: Number of MACE layers. Default is 2.
        num_channels: The number of channels. Default is 256.
        l_max: Highest harmonic order included in the Spherical Harmonics series.
               Default is 2.
        num_heads: Number of heads in the attention block. Default is 8.
        num_rbf: Number of basis functions used in the embedding block. Default is 32.
        trainable_rbf: Whether to add learnable weights to each of the radial embedding
                       basis functions. Default is ``False``.
        activation: Activation function for the output block. Options are "silu"
                    (default), "ssp" (which is shifted softplus), "tanh", "sigmoid", and
                    "swish".
        attn_activation: Activation function for the attention block. Options are "silu"
                         (default), "ssp" (which is shifted softplus), "tanh",
                         "sigmoid", and "swish".
        vecnorm_type: The type of the vector norm. The options are "max_min" (default)
                      and "rms".
        predict_stress: Whether to also predict stress when running the model.
                        If set to ``False`` (default), only compute energy and forces.
        atomic_energies: How to treat the atomic energies. If set to ``None`` (default)
                         or the string ``"average"``, then the average atomic energies
                         stored in the dataset info are used. It can also be set to the
                         string ``"zero"`` which means not to use any atomic energies
                         in the model. Lastly, one can also pass an atomic energies
                         dictionary via this parameter different from the one in the
                         dataset info, that is used.
        learnable_atomic_energies: Whether the atomic energies should be learnable,
                                   which is set to ``False`` as the default.
        num_species: The number of elements (atomic species descriptors) allowed.
                     If ``None`` (default), infer the value from the atomic energies
                     map in the dataset info.
        return_uninitialized_module: By default, this is ``False`` meaning that this
                                     function initializes the predictor module and
                                     returns its apply function and parameters.
                                     If ``True``, this function returns the module
                                     directly and has to be initialized downstream
                                     to obtain initial parameters. However, this
                                     second method allows for more inspection
                                     capabilities of the module if desired in downstream
                                     tasks.

    Returns:
        If ``return_uninitialized_module`` is ``False``, the predictor apply function
        and the initial parameters for it are returned. This is the default behavior.
        If ``return_uninitialized_module`` is ``True``, this function returns
        the :class:`~mlip_jax.models.predictor.ForceFieldPredictor` module directly,
        which then still has to be initialized downstream.
    """
    r_max = dataset_info.cutoff_distance_angstrom
    if num_species is None:
        num_species = len(dataset_info.atomic_energies_map)

    atomic_energies = get_atomic_energies(atomic_energies, dataset_info, num_species)

    visnet_kwargs = dict(
        lmax=l_max,
        vecnorm_type=vecnorm_type,
        num_heads=num_heads,
        num_layers=num_layers,
        hidden_channels=num_channels,
        num_rbf=num_rbf,
        rbf_type="expnorm",
        trainable_rbf=trainable_rbf,
        activation=activation,
        attn_activation=attn_activation,
        cutoff=r_max,
        vertex_type="Edge",
        num_species=num_species,
    )

    logging.info(f"Creating ViSNet with parameters: {visnet_kwargs}")

    visnet = Visnet(
        learnable_atomic_energies=learnable_atomic_energies,
        mean=dataset_info.scaling_mean,
        std=dataset_info.scaling_stdev,
        atomic_energies=atomic_energies,
        num_species=num_species,
        hidden_channels=num_channels,
        activation=activation,
        visnet_kwargs=visnet_kwargs,
    )

    predictor = ForceFieldPredictor(mlip_network=visnet, predict_stress=predict_stress)

    if return_uninitialized_module:
        return predictor

    params = predictor.init(
        jax.random.PRNGKey(initialize_seed),
        get_dummy_graph_for_model_init(),
    )

    return predictor.apply, params
