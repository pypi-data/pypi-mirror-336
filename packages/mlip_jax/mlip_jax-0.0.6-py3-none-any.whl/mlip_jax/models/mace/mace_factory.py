import logging
from typing import Optional, Union

import jax

from mlip_jax.data.dataset_info import DatasetInfo
from mlip_jax.data.helpers.dummy_init_graph import get_dummy_graph_for_model_init
from mlip_jax.models.atomic_energies import get_atomic_energies
from mlip_jax.models.mace.models import MACENet
from mlip_jax.models.predictor import ForceFieldPredictor
from mlip_jax.models.radial_embedding import (
    bessel_basis,
    polynomial_envelope_updated,
    soft_envelope,
)
from mlip_jax.models.type_aliases import ModelParameters, ModelPredictorFun


def _validate_and_unpack_readout_irreps(
    readout_irreps: tuple[str, ...]
) -> tuple[str, str]:
    if len(readout_irreps) != 2:
        raise ValueError("Readout irreps has to be of length 2 in the current version!")

    readout_hidden_irreps, output_irreps = readout_irreps

    if not isinstance(readout_hidden_irreps, str) or not isinstance(output_irreps, str):
        raise ValueError(
            "The representations inside the readout irreps must be of type string."
        )

    return readout_hidden_irreps, output_irreps


def create_mace_force_field(
    dataset_info: DatasetInfo,
    initialize_seed: int = 42,
    num_layers: int = 2,
    num_channels: int = 128,
    l_max: int = 3,
    node_symmetry: Optional[int] = None,
    correlation: int = 3,
    readout_irreps: tuple[str, ...] = ("16x0e", "0e"),
    num_readout_heads: int = 1,
    include_pseudotensors: bool = False,
    num_bessel: int = 8,
    activation: str = "silu",
    radial_envelope: str = "polynomial_envelope",
    symmetric_tensor_product_basis: bool = False,
    predict_stress: bool = False,
    atomic_energies: Optional[Union[str, dict[int, float]]] = None,
    avg_num_neighbors: Optional[float] = None,
    avg_r_min: Optional[float] = None,
    num_species: Optional[int] = None,
    return_uninitialized_module: bool = False,
) -> tuple[ModelPredictorFun, ModelParameters] | ForceFieldPredictor:
    """For the MACE model, by default, this creates the force field model predictor
    function and initial parameters for it. Alternatively, one can also get the
    uninitialized module returned directly by setting ``return_uninitialized_module``
    to ``True``.

    Args:
        dataset_info: The dataset info object obtained from the data preprocessing step.
        initialize_seed: A random seed for weight initialization. By default,
                         this is 42. Has no effect
                         if ``return_uninitialized_module`` is set to ``True``.
        num_layers: Number of MACE layers. Default is 2.
        num_channels: The number of channels. Default is 128.
        l_max: Highest degree of spherical harmonics used for the directional encoding
               of edge vectors, and during the convolution block. Default is 3, it is
               recommended to keep it at 3.
        node_symmetry: Highest degree of node features kept after the node-wise power
                       expansion of features, also called Atomic Cluster Expansion
                       (ACE). The default behaviour is to assign `l_max`, although
                       high values of `node_symmetry` may have a significant impact
                       on runtime. It should be less or equal to `l_max`.
        correlation: Maximum correlation order, by default it is 3.
        readout_irreps: Irreps for the readout block, passed as a tuple of irreps
                        string representations for each of the layers in the
                        readout block. Currently, this MACE model only supports
                        two layers, and it defaults to ``("16x0e", "0e")``.
        num_readout_heads: Number of readout heads. The default is 1. For fine-tuning,
                           additional heads must be added.
        include_pseudotensors: If ``False`` (default), only parities ``p = (-1)**l``
                               will be kept.
                               If ``True``, all parities will be kept,
                               e.g., ``"1e"`` pseudo-vectors returned by the cross
                               product on R3.
        num_bessel: The number of Bessel basis functions to use (default is 8).
        activation: The activation function used in the non-linear readout block.
                    The options are ``"silu"``, ``"elu"``, ``"relu"``, ``"tanh"``,
                    ``"sigmoid"``, and ``"swish"``. The default is ``"silu"``.
        radial_envelope: The radial envelope function, by default it
                         is ``"polynomial_envelope"``.
                         The only other option is ``"soft_envelope"``.
        symmetric_tensor_product_basis: Whether to use a symmetric tensor product basis
                                        (default is ``False``).
        predict_stress: Whether to also predict stress when running the model.
                        If set to ``False`` (default), only compute energy and forces.
        atomic_energies: How to treat the atomic energies. If set to ``None`` (default)
                         or the string ``"average"``, then the average atomic energies
                         stored in the dataset info are used. It can also be set to the
                         string ``"zero"`` which means not to use any atomic energies
                         in the model. Lastly, one can also pass an atomic energies
                         dictionary via this parameter different from the one in the
                         dataset info, that is used.
        avg_num_neighbors: The mean number of neighbors for atoms. If ``None``
                           (default), use the value from the dataset info.
                           It is used to rescale messages by this value.
        avg_r_min: The mean minimum neighbour distance in Angstrom. If ``None``
                   (default), use the value from the dataset info.
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
    if avg_r_min is None:
        avg_r_min = dataset_info.avg_r_min_angstrom
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

    if node_symmetry is None:
        node_symmetry = l_max
    elif node_symmetry > l_max:
        raise ValueError("Message symmetry must be lower or equal to 'l_max'")

    atomic_energies = get_atomic_energies(atomic_energies, dataset_info, num_species)

    readout_mlp_irreps, output_irreps = _validate_and_unpack_readout_irreps(
        readout_irreps
    )

    # TODO: the variables names must still be harmonised between the low-level
    # implementation and the user-facing interface.
    mace_kwargs = dict(
        r_max=r_max,
        num_channels=num_channels,
        avg_num_neighbors=avg_num_neighbors,
        num_interactions=num_layers,
        avg_r_min=avg_r_min,
        num_species=num_species,
        num_bessel=num_bessel,
        radial_basis=bessel_basis,
        radial_envelope=radial_envelope_fun,
        symmetric_tensor_product_basis=symmetric_tensor_product_basis,
        off_diagonal=False,
        l_max=l_max,
        node_symmetry=node_symmetry,
        include_pseudotensors=include_pseudotensors,
        num_readout_heads=num_readout_heads,
        readout_mlp_irreps=readout_mlp_irreps,
        correlation=correlation,
        gate=activation,
    )
    logging.info(f"Created MACE with parameters {mace_kwargs}")
    mace_net = MACENet(
        path_normalization="path",
        gradient_normalization="path",
        mace_kwargs=mace_kwargs,
        mean=dataset_info.scaling_mean,
        std=dataset_info.scaling_stdev,
        atomic_energies=atomic_energies,
        num_species=num_species,
        output_irreps=output_irreps,
    )

    predictor = ForceFieldPredictor(
        mlip_network=mace_net, predict_stress=predict_stress
    )

    if return_uninitialized_module:
        return predictor

    params = predictor.init(
        jax.random.PRNGKey(initialize_seed),
        get_dummy_graph_for_model_init(),
    )

    return predictor.apply, params
