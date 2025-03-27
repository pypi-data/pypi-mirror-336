from typing import Callable, Optional, Tuple

import e3nn_jax as e3nn
import flax.linen as nn
import jax.numpy as jnp

from mlip_jax.models.mace.message_passing import MessagePassingConvolution
from mlip_jax.models.mace.symmetric_contraction import SymmetricContraction


class LinearReadoutBlock(nn.Module):
    output_irreps: e3nn.Irreps

    @nn.compact
    def __call__(self, x: e3nn.IrrepsArray) -> e3nn.IrrepsArray:
        output_irreps = e3nn.Irreps(self.output_irreps)
        # x = [n_nodes, irreps]
        return e3nn.flax.Linear(output_irreps)(x)  # [n_nodes, output_irreps]


class NonLinearReadoutBlock(nn.Module):
    hidden_irreps: e3nn.Irreps
    output_irreps: e3nn.Irreps
    activation: Optional[Callable] = None
    gate: Optional[Callable] = None

    @nn.compact
    def __call__(self, x: e3nn.IrrepsArray) -> e3nn.IrrepsArray:
        hidden_irreps = e3nn.Irreps(self.hidden_irreps)
        output_irreps = e3nn.Irreps(self.output_irreps)

        # x = [n_nodes, irreps]
        num_vectors = hidden_irreps.filter(
            drop=["0e", "0o"]
        ).num_irreps  # Multiplicity of (l > 0) irreps
        x = e3nn.flax.Linear(
            (hidden_irreps + e3nn.Irreps(f"{num_vectors}x0e")).simplify()
        )(x)
        x = e3nn.gate(x, even_act=self.activation, even_gate_act=self.gate)
        return e3nn.flax.Linear(output_irreps)(x)  # [n_nodes, output_irreps]


class EquivariantProductBasisBlock(nn.Module):
    target_irreps: e3nn.Irreps
    correlation: int
    num_species: int
    symmetric_tensor_product_basis: bool = True
    off_diagonal: bool = False

    @nn.compact
    def __call__(
        self,
        node_feats: e3nn.IrrepsArray,  # [n_nodes, feature * irreps]
        node_specie: jnp.ndarray,  # [n_nodes, ] int
    ) -> e3nn.IrrepsArray:
        target_irreps = e3nn.Irreps(self.target_irreps)
        node_feats = node_feats.mul_to_axis().remove_nones()
        node_feats = SymmetricContraction(
            keep_irrep_out={ir for _, ir in target_irreps},
            correlation=self.correlation,
            num_species=self.num_species,
            gradient_normalization="element",
            symmetric_tensor_product_basis=self.symmetric_tensor_product_basis,
            off_diagonal=self.off_diagonal,
        )(node_feats, node_specie)
        node_feats = node_feats.axis_to_mul()
        return e3nn.flax.Linear(target_irreps)(node_feats)


class InteractionBlock(nn.Module):
    target_irreps: e3nn.Irreps
    avg_num_neighbors: float
    l_max: int
    activation: Callable

    @nn.compact
    def __call__(
        self,
        vectors: e3nn.IrrepsArray,  # [n_edges, 3]
        node_feats: e3nn.IrrepsArray,  # [n_nodes, irreps]
        radial_embedding: jnp.ndarray,  # [n_edges, radial_embedding_dim]
        senders: jnp.ndarray,  # [n_edges, ]
        receivers: jnp.ndarray,  # [n_edges, ]
    ) -> Tuple[e3nn.IrrepsArray, e3nn.IrrepsArray]:
        assert node_feats.ndim == 2
        assert vectors.ndim == 2
        assert radial_embedding.ndim == 2

        target_irreps = e3nn.Irreps(self.target_irreps)

        node_feats = e3nn.flax.Linear(node_feats.irreps, name="linear_up")(node_feats)

        node_feats = MessagePassingConvolution(
            self.avg_num_neighbors,
            target_irreps,
            self.l_max,
            self.activation,
        )(vectors, node_feats, radial_embedding, senders, receivers)
        node_feats = e3nn.flax.Linear(target_irreps, name="linear_down")(node_feats)

        assert node_feats.ndim == 2
        return node_feats  # [n_nodes, target_irreps]


class ScaleShiftBlock(nn.Module):
    scale: float
    shift: float

    @nn.compact
    def __call__(self, x: e3nn.IrrepsArray) -> e3nn.IrrepsArray:
        return self.scale * x + self.shift

    def __repr__(self):
        return (
            f"{self.__class__.__name__}(scale={self.scale:.6f}, shift={self.shift:.6f})"
        )
