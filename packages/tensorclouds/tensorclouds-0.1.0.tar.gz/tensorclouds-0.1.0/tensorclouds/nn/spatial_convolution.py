from typing import Callable, List, Tuple

from einops import rearrange, repeat

import e3nn_jax as e3nn
from flax import linen as nn
import jax
import jax.numpy as jnp

from .residual import Residual
from .self_interaction import SelfInteraction

from .layer_norm import EquivariantLayerNorm
from .profile import profile
from ..tensorcloud import TensorCloud


class CompleteSpatialConvolution(nn.Module):

    irreps_out: e3nn.Irreps
    radial_cut: float
    radial_bins: int = 32
    radial_basis: str = "gaussian"
    edge_irreps: e3nn.Irreps = e3nn.Irreps("0e + 1e + 2e")
    norm: bool = True
    k_seq: int = 16
    attention: bool = False
    activation: Callable = jax.nn.silu
    move: bool = True

    @nn.compact
    def __call__(self, state: TensorCloud) -> TensorCloud:
        seq_len = state.irreps_array.shape[0]
        assert state.mask.shape == (seq_len,)
        assert state.coord.shape == (seq_len, 3)
        features = state.irreps_array
        coord = state.coord

        if seq_len == 1:
            print("[WARNING] Skipping Spatial Convolution - seq_len == 1")
            return state

        features_i = e3nn.IrrepsArray(
            features.irreps, repeat(features.array, "i h -> i j h", j=seq_len)
        )
        features_j = e3nn.IrrepsArray(
            features.irreps, repeat(features.array, "j h -> i j h", i=seq_len)
        )
        coord_i = repeat(coord, "i d -> i j d", j=seq_len)
        coord_j = repeat(coord, "j d -> i j d", i=seq_len)

        mask_coord_i = repeat(state.mask_coord, "i -> i j", j=seq_len)
        mask_coord_j = repeat(state.mask_coord, "j -> i j", i=seq_len)
        cross_mask = mask_coord_i & mask_coord_j

        vectors = (coord_i - coord_j) * cross_mask[..., None]
        norm_sqr = jnp.sum(vectors**2, axis=-1)
        norm = jnp.where(
            norm_sqr == 0.0, 0.0,
            jnp.sqrt(jnp.where(norm_sqr == 0.0, 1.0, norm_sqr))
        )


        # Angular embedding:
        ang_embed = e3nn.spherical_harmonics(
            self.edge_irreps, vectors, False, "component"
        )
        ang_embed = ang_embed * cross_mask[..., None].astype(ang_embed.array.dtype)

        # messages_i = e3nn.flax.Linear(self.irreps_out)(
        #     e3nn.tensor_product(ang_embed, features_i)
        # )

        messages_j = e3nn.flax.Linear(self.irreps_out)(
            e3nn.tensor_product(ang_embed, features_j)
        )


        messages = e3nn.concatenate([
            # messages_i,
            messages_j,
            ang_embed, 
        ], axis=-1).regroup()

        # Radial part:
        rad_embed = (
            e3nn.soft_one_hot_linspace(
                norm,
                start=0.0,
                end=self.radial_cut,
                number=self.radial_bins,
                basis=self.radial_basis,
                cutoff=True,
            )
            * cross_mask[..., None]
        )

        seq_pos_i = repeat(jnp.arange(seq_len), "i -> i j", j=seq_len)
        seq_pos_j = repeat(jnp.arange(seq_len), "j -> i j", i=seq_len)

        relative_seq_pos = seq_pos_i - seq_pos_j
        k_seq = self.k_seq

        relative_seq_pos = jnp.where(
            jnp.abs(relative_seq_pos) <= k_seq, relative_seq_pos, 0
        )
        relative_seq_pos = jnp.where(cross_mask, relative_seq_pos, 0)

        relative_seq_pos = relative_seq_pos + k_seq
        relative_seq_pos = nn.Embed(num_embeddings=2 * k_seq + 1, features=32)(
            relative_seq_pos
        )

        rad_embed = e3nn.concatenate([relative_seq_pos, rad_embed, messages.filter('0e')], axis=-1).regroup()
        rad_embed = e3nn.flax.MultiLayerPerceptron(
            [self.radial_bins, messages.irreps.num_irreps],
            self.activation,
            with_bias=True,
            output_activation=False,
        )(rad_embed)

        messages = (
            messages * rad_embed * cross_mask[..., None].astype(messages.array.dtype)
        )

        features_aggr = e3nn.sum(messages, axis=1) / (
            jnp.sum(cross_mask, axis=1, keepdims=True) + 1e-6
        )
        features_aggr = features_aggr * (jnp.sum(cross_mask, axis=1, keepdims=True) > 1)
        features = e3nn.flax.Linear(self.irreps_out)(features_aggr)

        if self.move:
            update = 1e-3 * e3nn.flax.Linear("1e")(features).array
            new_coord = state.coord + update
            state = state.replace(coord=new_coord)

        return state.replace(irreps_array=features)


def knn(coord: jax.Array, mask: jax.Array, k: int, k_seq: int = 0, k_rand: int = 0):
    n, d = coord.shape
    distance_matrix = jnp.sum(
        jnp.square(coord[:, None, :] - coord[None, :, :]), axis=-1
    )
    assert distance_matrix.shape == (n, n)
    matrix_mask = mask[:, None] & mask[None, :]
    assert matrix_mask.shape == (n, n)

    distance_matrix = jnp.where(matrix_mask, distance_matrix, jnp.inf)

    # if k sequence nearest neighbors is on:
    if k_seq != 0:
        seq_nei_matrix = jnp.zeros((n, n))
        eye = jnp.eye(n)
        for i in range(1, k_seq // 2 + 1):
            up = jnp.roll(eye, i, axis=0)
            down = jnp.roll(eye, -i, axis=0)
            up = up - jnp.triu(up, k=0)
            down = down - jnp.tril(down, k=0)
            seq_nei_matrix += up + down
        seq_nei_matrix = jnp.where(matrix_mask, seq_nei_matrix, 0)
        distance_matrix = jnp.where(seq_nei_matrix, -jnp.inf, distance_matrix)
        
    neg_dist, neighbors = jax.lax.top_k(-distance_matrix, k) # we include the self-convolution here
    mask = neg_dist != -jnp.inf

    return neighbors, mask


class kNNSpatialConvolution(nn.Module):

    irreps_out: e3nn.Irreps
    radial_cut: float
    radial_bins: int = 32
    radial_basis: str = "gaussian"
    edge_irreps: e3nn.Irreps = e3nn.Irreps("0e + 1e + 2e")
    norm: bool = True
    k_seq: int = 16
    k: int = 16
    k_rand: int = 0
    attention: bool = False
    activation: Callable = jax.nn.silu

    @nn.compact
    def __call__(self, state: TensorCloud) -> TensorCloud:
        seq_len = state.irreps_array.shape[0]
        assert state.irreps_array.shape == (seq_len, state.irreps_array.irreps.dim)
        assert state.mask.shape == (seq_len,)
        assert state.coord.shape == (seq_len, 3)
        irreps_in = state.irreps_array.irreps

        features = state.irreps_array
        if seq_len == 1:
            print("[WARNING] Skipping Spatial Convolution - seq_len == 1")
            return state

        # k nearest neighbors:
        k = min(self.k + 1, seq_len)
        nei_indices, nei_mask = knn(
            state.coord,
            state.mask_coord,
            k=k,
            k_seq=self.k_seq,
            k_rand=self.k_rand,
        )
        k = nei_indices.shape[1]

        # Embeddings:
        vectors = state.coord[nei_indices, :] - state.coord[:, None, :]
        norm_sqr = jnp.sum(vectors**2, axis=-1)
        norm = jnp.sqrt(jnp.where(norm_sqr == 0.0, 1.0, norm_sqr))

        # Angular embedding:
        ang_embed = e3nn.spherical_harmonics(
            self.edge_irreps, vectors, False, "component"
        )

        # Radial embedding:
        rad_embed = nei_mask[..., None] * e3nn.soft_one_hot_linspace(
            norm,
            start=0.0,
            end=self.radial_cut,
            number=self.radial_bins,
            basis=self.radial_basis,
            cutoff=True,
        )

        nei_states = nei_mask[:, :, None] * state.irreps_array[nei_indices, :]
        # Angular part:
        messages = e3nn.flax.Linear(self.irreps_out)(
            e3nn.concatenate(
                [e3nn.tensor_product(ang_embed, nei_states), ang_embed], axis=-1
            ).regroup()
        )

        # Radial part:
        features_expanded = repeat(features.filter("0e").array, "... d -> ... k d", k=k)
        rad_embed = e3nn.concatenate(
            [messages.filter("0e"), rad_embed, features_expanded], axis=-1
        ).regroup()
        mix = e3nn.flax.MultiLayerPerceptron(
            [self.radial_bins, messages.irreps.num_irreps],
            self.activation,
            with_bias=True,
            output_activation=False,
        )(rad_embed)

        # Sum over neighbors:
        features = e3nn.sum(messages * mix, axis=1) / k

        return state.replace(irreps_array=features)


# class IPA(nn.Module):
#     def __init__(
#         self,
#         irreps_out: e3nn.Irreps,
#         *,
#         radial_cut: float,
#         radial_bins: int = 32,
#         radial_basis: str = "fourier",
#         edge_irreps: e3nn.Irreps = e3nn.Irreps("0e + 1e + 2e"),
#         norm: bool = True,
#         attention: bool = False,
#         activation: Callable = jax.nn.silu,
#         move: bool = False,
#     ):
#         super().__init__()
#         self.irreps_out = e3nn.Irreps(irreps_out)
#         self.radial_cut = radial_cut
#         self.radial_bins = radial_bins
#         self.radial_basis = radial_basis
#         self.edge_irreps = e3nn.Irreps(edge_irreps)
#         self.norm = norm
#         self.activation = activation
#         self.attention = attention
#         self.move = move

#     def _call(self, state: TensorCloud) -> TensorCloud:
#         seq_len = state.irreps_array.shape[0]
#         assert state.mask.shape == (seq_len,)
#         assert state.coord.shape == (seq_len, 3)
#         irreps_in = state.irreps_array.irreps

#         features = state.irreps_array
#         coord = state.coord

#         if seq_len == 1:
#             print('[WARNING] Skipping Spatial Convolution - seq_len == 1')
#             return state

#         features_i = e3nn.IrrepsArray(features.irreps, repeat(features.array, 'i h -> i j h', j=seq_len))
#         features_j = e3nn.IrrepsArray(features.irreps, repeat(features.array, 'j h -> i j h', i=seq_len))

#         coord_i = repeat(coord, 'i d -> i j d', j=seq_len)
#         coord_j = repeat(coord, 'j d -> i j d', i=seq_len)

#         mask_coord_i = repeat(state.mask_coord, 'i -> i j', j=seq_len)
#         mask_coord_j = repeat(state.mask_coord, 'j -> i j', i=seq_len)
#         cross_mask = (mask_coord_i & mask_coord_j)

#         n_heads = 2
#         # irreps_attn = features_i.irreps // n_heads

#         # GENERALIZED INVARIANT POINT ATTENTION

#         # [ i j h d/h ]
#         keys = e3nn.flax.Linear(features_i.irreps)(features_i).mul_to_axis(n_heads)
#         queries = e3nn.flax.Linear(features_j.irreps)(features_j).mul_to_axis(n_heads)

#         # [ i j h d/h c ]
#         vec_keys = rearrange(keys.filter('1e').array, '... (d c) -> ... d c', c=3) + coord_i[..., None, None, :]
#         vec_queries = rearrange(queries.filter('1e').array, '... (d c) -> ... d c', c=3) + coord_j[..., None, None, :]

#         # [ i j h d/h c ]
#         delta_vecs = (vec_queries - vec_keys)

#         # [ i j h ]
#         vec_scores = -jnp.sum(delta_vecs**2, axis=(-1, -2))

#         # [ i j d ]
#         scalars_i = features_i.filter('0e')
#         scalars_j = features_j.filter('0e')

#         # [ i j d ] + [ i j d ] -> [ i j h d/h ]
#         scalars_i = scalars_i.mul_to_axis(n_heads)
#         scalars_j = scalars_j.mul_to_axis(n_heads)

#         # [ i j h ]
#         scalar_scores = jnp.sum(scalars_i * scalars_j, axis=-1)

#         # [ i j h ]
#         attention_scores = scalar_scores + vec_scores
#         attention = jnp.where(cross_mask[..., None], attention_scores, jnp.finfo(attention_scores.dtype).min)

#         # [ i j h ]
#         attention = jax.nn.softmax(attention, axis=-2)
#         attention = attention * cross_mask[..., None]

#         # [ i j 3 ]
#         delta_coord = (coord_j - coord_i) * cross_mask[..., None]
#         delta_coord = e3nn.IrrepsArray(e3nn.Irreps("1x1e"), delta_coord)

#         # [ i j h d/h ]
#         values = e3nn.flax.Linear(features_j.irreps)(
#             # [ i j h+3 ]
#             e3nn.concatenate([features_j, delta_coord], axis=-1).regroup()
#         ).mul_to_axis(n_heads)

#         # [ i j h d/h ] -> [ i h d/h ]
#         features_aggr = e3nn.sum(attention[..., None] * values, axis=1)

#         # [ i h d/h ] -> [ i d ]
#         features_aggr = features_aggr.axis_to_mul()

#         # [ i d ]
#         features = e3nn.flax.Linear(self.irreps_out)(features_aggr)

#         return state.replace(irreps_array=features)

#     def __call__(self, state: TensorCloud) -> TensorCloud:
#         state = Residual(self._call)(state)
#         if self.norm:
#             state = state.replace(
#                 irreps_array=EquivariantLayerNorm()(state.irreps_array))
#         return state
