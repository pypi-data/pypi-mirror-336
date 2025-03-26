import jax
import jax.numpy as jnp
from jax.tree_util import tree_map, tree_flatten, tree_unflatten, register_pytree_node

from typing import List, Tuple, Any
import numpy as np
import jax.numpy as jnp
import jaxlib


ACCEPTED_FORMATS = [
    np.ndarray,
    jax.Array,
    jaxlib.xla_extension.ArrayImpl,
    jax.interpreters.partial_eval.DynamicJaxprTracer,
    jax._src.interpreters.batching.BatchTracer,
    jax._src.core.ShapedArray,
]

import e3nn_jax as e3nn

ACCEPTED_TYPES = [np.float64, np.float32, np.int64, np.int32, np.bool_]


def register_pytree(Datum):
    def encode_datum_pytree(datum: Datum) -> List[Tuple]:
        attrs = []
        went_through = False
        for attr, obj in vars(datum).items():
            # NOTE(Allan): come back here and make it universal
            if (
                (type(obj) == object)
                or ((type(obj) in ACCEPTED_FORMATS) and (obj.dtype in ACCEPTED_TYPES))
                or (type(obj) == e3nn.IrrepsArray)
            ):
                went_through = True
                attrs.append(obj)
            else:
                attrs.append(None)
        if not went_through:
            breakpoint()
        return attrs, vars(datum).keys()

    def decode_datum_pytree(keys, values: List[Any]) -> Datum:
        return Datum(**dict(zip(keys, values)))

    register_pytree_node(Datum, encode_datum_pytree, decode_datum_pytree)


def l2_norm(tree):
    """Compute the l2 norm of a pytree of arrays. Useful for weight decay."""
    leaves, _ = tree_flatten(tree)
    return jnp.sqrt(sum(jnp.vdot(x, x) for x in leaves))


def clip_grads(grad_tree, max_norm):
    """Clip gradients stored as a pytree of arrays to maximum norm `max_norm`."""
    norm = l2_norm(grad_tree)
    normalize = lambda g: jnp.where(norm < max_norm, g, g * (max_norm / norm))
    return tree_map(normalize, grad_tree)


def inner_stack(pytrees):
    return jax.tree_util.tree_map(lambda *values: jnp.stack(values, axis=0), *pytrees)


def inner_split(pytree):
    leaves, defs = tree_flatten(pytree)
    splits = [
        [arr.squeeze(0) for arr in jnp.split(leaf, len(leaf), axis=0)]
        for leaf in leaves
    ]
    splits = list(zip(*splits))
    return [tree_unflatten(defs, split) for split in splits]
