import logging
from typing import Optional, Union

import jax

from mlip_jax.data.dataset_info import DatasetInfo
from mlip_jax.data.helpers.dummy_init_graph import get_dummy_graph_for_model_init
from mlip_jax.models.atomic_energies import get_atomic_energies
from mlip_jax.models.nequip.models import NequIPNet
from mlip_jax.models.predictor import ForceFieldPredictor
from mlip_jax.models.radial_embedding import (
    bessel_basis,
    polynomial_envelope_updated,
    soft_envelope,
)
from mlip_jax.models.type_aliases import ModelParameters, ModelPredictorFun


def create_nequip_force_field(
    dataset_info: DatasetInfo,
    initialize_seed: int = 42,
    num_layers: int = 2,
    hidden_irreps: str = "128x0e + 64x1e + 4x2e",
    sh_irreps: str = "1x0e + 1x1e + 1x2e",
    num_bessel: int = 8,
    radial_net_nonlinearity: str = "raw_swish",
    radial_net_n_hidden: int = 64,
    radial_net_n_layers: int = 2,
    radial_envelope: str = "polynomial_envelope",
    scalar_mlp_std: float = 4.0,
    predict_stress: bool = False,
    atomic_energies: Optional[Union[str, dict[int, float]]] = None,
    learnable_atomic_energies: bool = False,
    avg_num_neighbors: Optional[float] = None,
    num_species: Optional[int] = None,
    return_uninitialized_module: bool = False,
) -> tuple[ModelPredictorFun, ModelParameters] | ForceFieldPredictor:
    """For the NequIP model, by default, this creates the force field model predictor
    function and initial parameters for it. Alternatively, one can also get the
    uninitialized module returned directly by setting ``return_uninitialized_module``
    to ``True``.

    Args:
        dataset_info: The dataset info object obtained from the data preprocessing step.
        initialize_seed: A random seed for weight initialization. By default,
                         this is 42. Has no effect
                         if ``return_uninitialized_module`` is set to ``True``.
        num_layers: Number of NequIP layers. Default is 2.
        hidden_irreps: The number of channels for each irrep order.
                       Default is 128 for l0, 64 for l1 and 4 for l2. This is
                       specified as "128x0e + 64x1e + 4x2e".
        sh_irreps: Default projections for edge embedding into spherical harmonics.
                   Default is up to l2, specified as ""1x0e + 1x1e + 1x2e".
        num_bessel: The number of Bessel basis functions to use (default is 8).
        radial_net_nonlinearity: Activation function for radial MLP.
                                 Default is raw_swish.
        radial_net_n_hidden: Number of hidden features in radial MLP. Default is 64.
        radial_net_n_layers: Number of layers in radial MLP. Default is 2.
        radial_envelope: The radial envelope function, by default it
                         is ``"polynomial_envelope"``.
                         The only other option is ``"soft_envelope"``.
        scalar_mlp_std: Standard deviation of weight init. of radial MLP.
                        Default is 4.0.
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
        avg_num_neighbors: The mean number of neighbors for atoms. If ``None``
                           (default), use the value from the dataset info.
                           It is used to rescale messages by this value.
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
    if avg_num_neighbors is None:
        avg_num_neighbors = dataset_info.avg_num_neighbors
    if num_species is None:
        num_species = len(dataset_info.atomic_energies_map)

    if radial_envelope == "soft_envelope":
        radial_envelope_fun = soft_envelope
    elif radial_envelope == "polynomial_envelope":
        radial_envelope_fun = polynomial_envelope_updated
    else:
        raise ValueError(
            "Radial envelope unknown. It should either be 'soft_envelope' "
            "or 'polynomial_envelope'."
        )

    atomic_energies = get_atomic_energies(atomic_energies, dataset_info, num_species)

    nequip_kwargs = dict(
        avg_num_neighbors=avg_num_neighbors,
        num_layers=num_layers,
        num_species=num_species,
        hidden_irreps=hidden_irreps,
        sh_irreps=sh_irreps,
        num_bessel=num_bessel,
        r_max=r_max,
        radial_net_nonlinearity=radial_net_nonlinearity,
        radial_net_n_hidden=radial_net_n_hidden,
        radial_net_n_layers=radial_net_n_layers,
        use_sc=True,
        nonlinearities={"e": "raw_swish", "o": "tanh"},
        avg_r_min=None,
        radial_basis=bessel_basis,
        radial_envelope=radial_envelope_fun,
        scalar_mlp_std=scalar_mlp_std,
    )
    logging.info(f"Created NequIP with parameters {nequip_kwargs}")
    nequip = NequIPNet(
        path_normalization="path",
        gradient_normalization="path",
        nequip_kwargs=nequip_kwargs,
        learnable_atomic_energies=learnable_atomic_energies,
        mean=dataset_info.scaling_mean,
        std=dataset_info.scaling_stdev,
        atomic_energies=atomic_energies,
    )

    predictor = ForceFieldPredictor(mlip_network=nequip, predict_stress=predict_stress)

    if return_uninitialized_module:
        return predictor

    params = predictor.init(
        jax.random.PRNGKey(initialize_seed),
        get_dummy_graph_for_model_init(),
    )

    return predictor.apply, params
