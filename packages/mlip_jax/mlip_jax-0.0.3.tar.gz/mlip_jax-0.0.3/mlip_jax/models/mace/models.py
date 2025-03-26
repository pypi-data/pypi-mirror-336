import functools
import math
from typing import Callable, Dict, Optional, Union

import e3nn_jax as e3nn
import flax.linen as nn
import jax
import jax.numpy as jnp

from mlip_jax.models.blocks import (
    FullyConnectedTensorProduct,
    LinearNodeEmbeddingBlock,
    RadialEmbeddingBlock,
)
from mlip_jax.models.mace.blocks import (
    EquivariantProductBasisBlock,
    InteractionBlock,
    LinearReadoutBlock,
    NonLinearReadoutBlock,
)
from mlip_jax.utils.safe_norm import safe_norm


def parse_activation(activation: str) -> Callable:  # TODO probably move to utils
    if activation == "silu":
        return jax.nn.silu
    elif activation == "elu":
        return jax.nn.elu
    elif activation == "relu":
        return jax.nn.relu
    elif activation == "tanh":
        return jax.nn.tanh
    elif activation == "sigmoid":
        return jax.nn.sigmoid
    elif activation == "swish":
        return jax.nn.swish
    else:
        raise ValueError(f"Unknown activation function {activation}")


class MACENet(nn.Module):
    """Wraps a `MACE` module, adding node contributions and atomic energies.

    The `mean` and `std` attributes are also used to rescale normalized
    outputs to the target distribution.

        # actually sum over nodes AND number of layers
        mace_net(r, z) = sum(mace'(r, z)[i] + E0[z[i]] for i in nodes)
        # rescale outputs *node-wise*
        mace'(r, z) = mean + mace(r, z) * std
    """

    path_normalization: str
    gradient_normalization: str
    mace_kwargs: Dict[
        str, Union[int, float, str, Callable[[int, int, int], jnp.ndarray]]
    ]
    learnable_atomic_energies: bool
    mean: float
    std: float
    atomic_energies: float
    num_species: int
    output_irreps: str

    @nn.compact
    def __call__(
        self,
        vectors: jnp.ndarray,
        node_z: jnp.ndarray,
        senders: jnp.ndarray,
        receivers: jnp.ndarray,
    ) -> jnp.ndarray:
        e3nn.config("path_normalization", self.path_normalization)
        e3nn.config("gradient_normalization", self.gradient_normalization)
        mace_kwargs = dict(self.mace_kwargs)
        gate = parse_activation(mace_kwargs["gate"])
        mace_kwargs["gate"] = gate
        mace = MACE(output_irreps=self.output_irreps, **mace_kwargs)

        contributions = mace(
            vectors, node_z, senders, receivers
        )  # [n_nodes, num_interactions, num_heads, 0e]

        contributions = contributions.array[
            :, :, :, 0
        ]  # [n_nodes, num_interactions, num_heads]
        sum_over_heads = jnp.sum(contributions, axis=2)  # [n_nodes, num_interactions]
        node_energies = jnp.sum(sum_over_heads, axis=1)  # [n_nodes, ]

        node_energies = self.mean + self.std * node_energies

        if self.learnable_atomic_energies:
            atomic_energies_ = self.param(
                "atomic_energies",
                nn.initializers.constant(self.atomic_energies)(
                    self.num_species,
                ),
            )
        else:
            atomic_energies_ = jnp.asarray(self.atomic_energies)
        node_energies += atomic_energies_[node_z]  # [n_nodes, ]

        return node_energies


class MACE(nn.Module):
    output_irreps: e3nn.Irreps  # Irreps of the output, default 1x0e
    r_max: float
    num_interactions: int  # Number of interactions (layers), default 2
    hidden_irreps: e3nn.Irreps  # 256x0e or 128x0e + 128x1o
    readout_mlp_irreps: (
        e3nn.Irreps
    )  # Hidden irreps of the MLP in last readout, default 16x0e
    avg_num_neighbors: float
    num_species: int
    radial_basis: Callable[[jnp.ndarray], jnp.ndarray]
    radial_envelope: Callable[[jnp.ndarray], jnp.ndarray]
    num_bessel: int = 8
    num_features: int = (
        None  # Number of features per node, default gcd of hidden_irreps multiplicities
    )
    avg_r_min: float = None
    # Number of zero derivatives at small and large distances, default 4 and 2
    # If both are None, it uses a smooth C^inf envelope function
    max_ell: int = 3  # Max spherical harmonic degree, default 3
    epsilon: Optional[float] = None
    correlation: int = (
        3  # Correlation order at each layer (~ node_features^correlation), default 3
    )
    gate: Callable = jax.nn.silu  # activation function
    soft_normalization: Optional[float] = None
    symmetric_tensor_product_basis: bool = True
    off_diagonal: bool = False
    interaction_irreps: Union[str, e3nn.Irreps] = "o3_restricted"  # or o3_full
    node_embedding: nn.Module = LinearNodeEmbeddingBlock
    num_readout_heads: int = 1
    residual_connection_first_layer: bool = False

    @nn.compact
    def __call__(
        self,
        vectors: e3nn.IrrepsArray,  # [n_edges, 3]
        node_specie: jnp.ndarray,  # [n_nodes] int between 0 and num_species-1
        senders: jnp.ndarray,  # [n_edges]
        receivers: jnp.ndarray,  # [n_edges]
        node_mask: Optional[jnp.ndarray] = None,  # [n_nodes] only used for profiling
    ) -> e3nn.IrrepsArray:
        assert vectors.ndim == 2 and vectors.shape[1] == 3
        assert node_specie.ndim == 1
        assert senders.ndim == 1 and receivers.ndim == 1
        assert vectors.shape[0] == senders.shape[0] == receivers.shape[0]

        if node_mask is None:
            node_mask = jnp.ones(node_specie.shape[0], dtype=jnp.bool_)

        output_irreps = e3nn.Irreps(self.output_irreps)
        hidden_irreps = e3nn.Irreps(self.hidden_irreps)
        readout_mlp_irreps = e3nn.Irreps(self.readout_mlp_irreps)

        num_features = self.num_features  # NOTE num_features is num_channels
        if num_features is None:
            num_features = functools.reduce(math.gcd, (mul for mul, _ in hidden_irreps))
            hidden_irreps = e3nn.Irreps(
                [(mul // num_features, ir) for mul, ir in hidden_irreps]
            )

        interaction_irreps = self.interaction_irreps
        if interaction_irreps == "o3_restricted":
            interaction_irreps = e3nn.Irreps.spherical_harmonics(self.max_ell)
        elif interaction_irreps == "o3_full":
            interaction_irreps = e3nn.Irreps(e3nn.Irrep.iterator(self.max_ell))
        else:
            interaction_irreps = e3nn.Irreps(interaction_irreps)

        # Embeddings
        node_embedding = self.node_embedding(
            self.num_species, num_features * hidden_irreps
        )
        radial_embedding = RadialEmbeddingBlock(
            r_max=self.r_max,
            avg_r_min=self.avg_r_min,
            basis_functions=self.radial_basis,
            envelope_function=self.radial_envelope,
            num_bessel=self.num_bessel,
        )

        # Embeddings
        node_feats = node_embedding(node_specie).astype(
            vectors.dtype
        )  # [n_nodes, feature * irreps]

        if not (hasattr(vectors, "irreps") and hasattr(vectors, "array")):
            vectors = e3nn.IrrepsArray("1o", vectors)

        radial_embedding = radial_embedding(safe_norm(vectors.array, axis=-1))

        # Interactions
        outputs = []
        for i in range(self.num_interactions):
            selector_tp = (i == 0) and not self.residual_connection_first_layer
            last_layer = i == self.num_interactions - 1

            i_hidden_irreps = (
                hidden_irreps if not last_layer else hidden_irreps.filter(output_irreps)
            )

            node_outputs, node_feats = MACELayer(
                selector_tp=selector_tp,
                last_layer=last_layer,
                num_features=num_features,
                interaction_irreps=interaction_irreps,
                hidden_irreps=i_hidden_irreps,
                max_ell=self.max_ell,
                avg_num_neighbors=self.avg_num_neighbors,
                activation=self.gate,
                num_species=self.num_species,
                epsilon=self.epsilon,
                correlation=self.correlation,
                output_irreps=output_irreps,
                readout_mlp_irreps=readout_mlp_irreps,
                symmetric_tensor_product_basis=self.symmetric_tensor_product_basis,
                off_diagonal=self.off_diagonal,
                soft_normalization=self.soft_normalization,
                name=f"layer_{i}",
                num_readout_heads=self.num_readout_heads,
            )(
                vectors,
                node_feats,
                node_specie,
                radial_embedding,
                senders,
                receivers,
                node_mask,
            )
            outputs += [node_outputs]  # list of [n_nodes, num_heads, output_irreps]

        return e3nn.stack(
            outputs, axis=1
        )  # [n_nodes, num_interactions, num_heads, output_irreps]


class MACELayer(nn.Module):
    selector_tp: bool
    last_layer: bool
    num_features: int
    interaction_irreps: e3nn.Irreps
    hidden_irreps: e3nn.Irreps
    activation: Callable
    num_species: int
    epsilon: Optional[float]
    name: Optional[str]
    # InteractionBlock:
    max_ell: int
    avg_num_neighbors: float
    # EquivariantProductBasisBlock:
    correlation: int
    symmetric_tensor_product_basis: bool
    off_diagonal: bool
    soft_normalization: Optional[float]
    # ReadoutBlock:
    output_irreps: e3nn.Irreps
    readout_mlp_irreps: e3nn.Irreps
    num_readout_heads: int = 1

    @nn.compact
    def __call__(
        self,
        vectors: e3nn.IrrepsArray,  # [n_edges, 3]
        node_feats: e3nn.IrrepsArray,  # [n_nodes, irreps]
        node_specie: jnp.ndarray,  # [n_nodes] int between 0 and num_species-1
        radial_embedding: jnp.ndarray,  # [n_edges, radial_embedding_dim]
        senders: jnp.ndarray,  # [n_edges]
        receivers: jnp.ndarray,  # [n_edges]
        node_mask: Optional[jnp.ndarray] = None,  # [n_nodes] only used for profiling
    ):
        interaction_irreps = e3nn.Irreps(
            self.interaction_irreps
        )  # TODO Explore overlap in irreps variable
        hidden_irreps = e3nn.Irreps(self.hidden_irreps)
        output_irreps = e3nn.Irreps(self.output_irreps)
        readout_mlp_irreps = e3nn.Irreps(self.readout_mlp_irreps)

        identity = jnp.eye(self.num_species)
        node_attr = identity[node_specie]

        if node_mask is None:
            node_mask = jnp.ones(node_specie.shape[0], dtype=jnp.bool_)

        # residual connection:
        residual_connection = None

        if not self.selector_tp:
            # Setting output_irreps
            if self.last_layer:
                residual_connection_irrep_out = (
                    self.num_features
                    * e3nn.Irreps(hidden_irreps).filter("0e").regroup()
                )
            else:
                residual_connection_irrep_out = (
                    self.num_features * e3nn.Irreps(self.interaction_irreps).regroup()
                )

            residual_connection = FullyConnectedTensorProduct(
                irreps_in1=node_feats.irreps,
                irreps_in2=self.num_species * e3nn.Irreps("0e"),
                irreps_out=residual_connection_irrep_out,
            )(x1=node_feats, x2=node_attr)

        # Interaction block
        node_feats = InteractionBlock(
            target_irreps=self.num_features * interaction_irreps,
            avg_num_neighbors=self.avg_num_neighbors,
            max_ell=self.max_ell,
            activation=self.activation,
        )(
            vectors=vectors,
            node_feats=node_feats,
            radial_embedding=radial_embedding,
            receivers=receivers,
            senders=senders,
        )

        # selector tensor product (first layer only)
        if self.selector_tp:
            node_feats = FullyConnectedTensorProduct(
                irreps_in1=self.num_features
                * e3nn.Irreps(self.interaction_irreps).regroup(),
                irreps_in2=self.num_species * e3nn.Irreps("0e"),
                irreps_out=self.num_features
                * e3nn.Irreps(self.interaction_irreps).regroup(),
            )(x1=node_feats, x2=node_attr)

        # EPBB
        if self.last_layer:
            node_feats = EquivariantProductBasisBlock(
                target_irreps=self.num_features * e3nn.Irreps("0e"),
                correlation=self.correlation,
                num_species=self.num_species,
                symmetric_tensor_product_basis=self.symmetric_tensor_product_basis,
                off_diagonal=self.off_diagonal,
            )(node_feats=node_feats, node_specie=node_specie)
        else:
            node_feats = EquivariantProductBasisBlock(
                target_irreps=self.num_features
                * e3nn.Irreps(self.interaction_irreps).regroup(),
                correlation=self.correlation,
                num_species=self.num_species,
                symmetric_tensor_product_basis=self.symmetric_tensor_product_basis,
                off_diagonal=self.off_diagonal,
            )(node_feats=node_feats, node_specie=node_specie)

        if self.soft_normalization is not None:

            def phi(n):
                n = n / self.soft_normalization
                return 1.0 / (1.0 + n * e3nn.sus(n))

            node_feats = e3nn.norm_activation(
                node_feats, [phi] * len(node_feats.irreps)
            )
        if residual_connection is not None:
            node_feats = (
                node_feats + residual_connection
            )  # [n_nodes, feature * hidden_irreps]

        # Multi-head readout
        node_outputs = []

        if not self.last_layer:
            for _head_idx in range(self.num_readout_heads):
                node_outputs += [
                    LinearReadoutBlock(output_irreps)(node_feats)
                ]  # [n_nodes, output_irreps]
        else:  # Non-linear readout for last layer
            for _head_idx in range(self.num_readout_heads):
                node_outputs += [
                    NonLinearReadoutBlock(
                        readout_mlp_irreps,
                        output_irreps,
                        activation=self.activation,
                    )(node_feats)
                ]  # [n_nodes, output_irreps]

        node_outputs = e3nn.stack(
            node_outputs, axis=1
        )  # [n_nodes, num_heads, output_irreps]

        return node_outputs, node_feats
