from typing import Callable
from typing import Union

import e3nn_jax as e3nn
from flax import linen as nn
import jax

from ..tensorcloud import TensorCloud


class Residual(nn.Module):

    function: Callable[[TensorCloud], TensorCloud]

    @nn.compact
    def __call__(self, state: TensorCloud) -> TensorCloud:
        assert state.irreps_array.ndim == 2
        assert state.mask.ndim == 1
        assert state.coord.ndim == 2

        new_state = self.function(state)

        seq_len = state.irreps_array.shape[0]
        new_seq_len = new_state.irreps_array.shape[0]

        if new_seq_len > seq_len:
            raise ValueError("Residual block cannot increase sequence length")

        if new_seq_len < seq_len:
            if (seq_len - new_seq_len) % 2 != 0:
                raise ValueError(
                    "Residual block cannot decrease sequence length by odd number"
                )

            pad = (seq_len - new_seq_len) // 2
            state = jax.tree_util.tree_map(lambda x: x[pad:-pad], state)

        if state.irreps_array.irreps == new_state.irreps_array.irreps:
            features = state.irreps_array + new_state.irreps_array
        else:
            features = e3nn.flax.Linear(new_state.irreps_array.irreps)(
                e3nn.concatenate(
                    [
                        state.irreps_array,
                        new_state.irreps_array,
                    ]
                )
            )

        return new_state.replace(irreps_array=features)
