from typing import Optional

import jax.numpy as jnp


def safe_norm(
    x: jnp.ndarray, axis: Optional[int] = None, keepdims: bool = False
) -> jnp.ndarray:
    """nan-safe norm."""
    x2 = jnp.sum(x**2, axis=axis, keepdims=keepdims)
    return jnp.where(x2 == 0.0, 0.0, jnp.where(x2 == 0, 1.0, x2) ** 0.5)
