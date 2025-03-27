import e3nn_jax as e3nn
import jax
import jax.numpy as jnp


def soft_envelope(
    length, max_length, arg_multiplicator: float = 2.0, value_at_origin: float = 1.2
):
    """Soft envelope radial envelope function."""
    return e3nn.soft_envelope(
        length,
        max_length,
        arg_multiplicator=arg_multiplicator,
        value_at_origin=value_at_origin,
    )


def bessel_basis(length: jax.Array, max_length: float, number: int) -> jax.Array:
    """Returns the Bessel function with given length, max. length, and number."""
    return e3nn.bessel(length, number, max_length)


def polynomial_envelope_updated(length: jax.Array, max_length: float, p: int = 5):
    """
    From the MACE torch version, referenced to:
    Klicpera, J.; Groß, J.; Günnemann, S.
    Directional Message Passing for Molecular Graphs; ICLR 2020.
    Equation (8)
    """

    def fun(x):
        envelope = (
            1.0
            - ((p + 1.0) * (p + 2.0) / 2.0) * jnp.pow(x / max_length, p)
            + p * (p + 2.0) * jnp.pow(x / max_length, p + 1)
            - (p * (p + 1.0) / 2) * jnp.pow(x / max_length, p + 2)
        )
        return envelope * (x < max_length)

    return fun(length)
