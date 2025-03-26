import functools
import operator
from typing import Callable, Optional

import e3nn_jax as e3nn
import flax.linen as nn
import jax
from jax.nn import initializers
from jax_md import util

tree_map = functools.partial(
    jax.tree.map, is_leaf=lambda x: isinstance(x, e3nn.IrrepsArray)
)
UnaryFn = Callable[[util.Array], util.Array]


class BetaSwish(nn.Module):

    @nn.compact
    def __call__(self, x):
        features = x.shape[-1]
        beta = self.param("Beta", nn.initializers.ones, (features,))
        return x * nn.sigmoid(beta * x)


NONLINEARITY_MAPPING = {
    "none": lambda x: x,
    "relu": nn.relu,
    "swish": BetaSwish(),
    "raw_swish": nn.swish,
    "tanh": nn.tanh,
    "sigmoid": nn.sigmoid,
    "silu": nn.silu,
}


def normal(var):
    return initializers.variance_scaling(var, "fan_in", "normal")


def get_nonlinearity_by_name(name: str) -> UnaryFn:
    if name in NONLINEARITY_MAPPING:
        return NONLINEARITY_MAPPING[name]
    raise ValueError(f"Nonlinearity '{name}' not found.")


def prod(xs):
    """From e3nn_jax/util/__init__.py."""
    return functools.reduce(operator.mul, xs, 1)


def tp_path_exists(arg_in1, arg_in2, arg_out):
    """Check if a tensor product path is viable.

    This helper function is similar to the one used in:
    https://github.com/e3nn/e3nn
    """
    arg_in1 = e3nn.Irreps(arg_in1).simplify()
    arg_in2 = e3nn.Irreps(arg_in2).simplify()
    arg_out = e3nn.Irrep(arg_out)

    for _multiplicity_1, irreps_1 in arg_in1:
        for _multiplicity_2, irreps_2 in arg_in2:
            if arg_out in irreps_1 * irreps_2:
                return True
    return False


class MLP(nn.Module):
    """Multilayer Perceptron."""

    features: tuple[int, ...]
    nonlinearity: str

    use_bias: bool = True
    scalar_mlp_std: Optional[float] = None

    @nn.compact
    def __call__(self, x):
        features = self.features

        dense = functools.partial(nn.Dense, use_bias=self.use_bias)
        phi = get_nonlinearity_by_name(self.nonlinearity)

        kernel_init = normal(self.scalar_mlp_std)

        for h in features[:-1]:
            x = phi(dense(h, kernel_init=kernel_init)(x))

        return dense(features[-1], kernel_init=normal(1.0))(x)
