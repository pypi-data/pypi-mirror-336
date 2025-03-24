# -------------------------------------------------------------------------------
# (c) Copyright 2023 Sony Semiconductor Israel, Ltd. All rights reserved.
#
#      This software, in source or object form (the "Software"), is the
#      property of Sony Semiconductor Israel Ltd. (the "Company") and/or its
#      licensors, which have all right, title and interest therein, You
#      may use the Software only in accordance with the terms of written
#      license agreement between you and the Company (the "License").
#      Except as expressly stated in the License, the Company grants no
#      licenses by implication, estoppel, or otherwise. If you are not
#      aware of or do not agree to the License terms, you may not use,
#      copy or modify the Software. You may use the source code of the
#      Software only for your internal purposes and may not distribute the
#      source code of the Software, any part thereof, or any derivative work
#      thereof, to any third party, except pursuant to the Company's prior
#      written consent.
#      The Software is the confidential information of the Company.
# -------------------------------------------------------------------------------
'''
Created on 2/15/23

@author: zvikaa
'''
from typing import List, Dict, Any

import numpy as np


from uni_model.auto_generated import Shape
from uni_model.auto_generated.ShapeImpl import ShapeImpl
from uni_model.auto_generated.Dtype import Dtype
from uni_model.auto_generated.UniLayerConst import UniLayerConst


def uni_const_from_numpy(name: str, data: np.ndarray, dtype: Dtype) -> UniLayerConst:
    shape = ShapeImpl(list(data.shape))
    if not shape:
        shape = ShapeImpl([1])
        data = (data.item())
    # tensor = UniTensor(shape, data.flatten().tolist(), uni_dtype)
    return UniLayerConst(name, float_data=data.flatten().tolist(), indices_data=[], out_dtypes=[dtype], out_shapes=[shape])


def create_const_with_float_data(name: str, float_data: List[float], dtype: Dtype, out_shapes: List[Shape] = None,
                                 out_dtypes: List[Dtype] = None,
                                 history: List[str] = None, attr: Dict[str, Any] = None) -> UniLayerConst:
    if out_shapes is None:
        out_shapes = []
    if out_dtypes is None:
        out_dtypes = []
    if history is None:
        history = []
    if attr is None:
        attr = {}
    return UniLayerConst(name, float_data, [], out_shapes, [dtype], history, attr)


def create_const_with_indices_data(name: str, indices_data: List[int], dtype: Dtype, out_shapes: List[Shape] = None,
                                   history: List[str] = None, attr: Dict[str, Any] = None) -> UniLayerConst:
    if out_shapes is None:
        out_shapes = []
    if history is None:
        history = []
    if attr is None:
        attr = {}

    return UniLayerConst(name, [], indices_data, out_shapes, [dtype], history, attr)
