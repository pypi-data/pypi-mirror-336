# Copyright 2016-2024 Cerebras Systems
# SPDX-License-Identifier: BSD-3-Clause

import torch

from cerebras.pytorch.decomp.registry import register_decomposition

# to be decorated on decompositions for ops that have overloads with extra parameters
from torch._prims_common.wrappers import out_wrapper  # noqa


aten = torch._ops.ops.aten


@register_decomposition(aten._weight_norm_interface)
def _weight_norm_interface(v, g, dim=0):
    """
    Decomposition for torch.aten._weight_norm_interface copied from PyTorch:
        https://github.com/pytorch/pytorch/blob/main/torch/_decomp/decompositions.py#L4993-L4999

    This implementation removes the line that does dtype checking:
        norm_dtype = torch.float if g.dtype == torch.bfloat16 else None
    as it is CUDA specific.
    """
    keep_dim = tuple(i for i in range(len(v.shape)) if i != dim)
    norm = v.norm(2, keep_dim, keepdim=True)
    return v * (g / norm.to(g.dtype)), norm
