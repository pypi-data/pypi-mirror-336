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

# This class is auto-generated in PythonGenerator of UniModel. Please don't change
from dataclasses import dataclass
import numpy as np
from uni_model.validation.validation_cfg import ValidationCfg
from uni_model.validation.error_builder import ErrorBuilder
from uni_model.validation.error_codes import ErrorCodes
from uni_model.validation.uni_model_exception import UniModelException
from typing import List, ClassVar
from uni_model.auto_generated.Shape import Shape
from uni_model.model.uni_layer import UniLayerBase, UniLayer
from uni_model.utils.immute import immute
from uni_model.converter.nodedef_generator import NodeDefGenerator
from uni_model.org.tensorflow.framework.attr_value_pb2 import AttrValue


@dataclass(frozen=True)
class _UniLayerBaseConst(UniLayerBase):
	float_data: List[float]
	indices_data: List[int]
	out_shapes: List[Shape]


@dataclass(frozen=True)
class UniLayerConst(UniLayer, _UniLayerBaseConst):
	op: ClassVar = "Const"
	_valid_input_range: ClassVar = range(0, 1)
	output_names: ClassVar = [""]

	def __eq__(self, other):
		if self.name != other.name or not np.allclose(self.float_data, other.float_data) or self.indices_data != other.indices_data or self.dtype != other.dtype or self.out_shapes != other.out_shapes or self.history != other.history or any([v != other.extended_attr[k] if not isinstance(v, float) else not np.allclose(v, other.extended_attr[k]) for k, v in self.extended_attr.items()]):
			return False
		return True

	def validate(self, validation_cfg: ValidationCfg, error_builder: ErrorBuilder, graph_id: str):
		super().validate(validation_cfg, error_builder, graph_id)
		if len(self.indices_data) > 0:
			legal_range = range(0, 2**self.dtype.value_n_bits)
			not_in_range = [index for index in self.indices_data if index not in legal_range]
			if len(not_in_range) > 0:
				raise UniModelException(ErrorCodes.CIDMBIN, f"Node const {self.name} forbidden indices: {not_in_range}. Used {self.dtype.value_n_bits} valueNBits. {ErrorCodes.CIDMBIN.value}")
		self.dtype.validate(validation_cfg, error_builder, graph_id, self)

	def __post_init__(self):
		if len(self.out_dtypes) != 1:
			raise UniModelException(message="out_dtypes list must be with size 1")
		super().__post_init__()

	def __hash__(self):
		return hash((self.name, tuple(np.array(self.float_data, dtype='float32')), tuple(self.indices_data), self.dtype, tuple(self.out_shapes), tuple(self.history), immute(self.extended_attr)))

	@property
	def dtype(self):
		return self.out_dtypes[0]

	def _match_correct_type_to_attr(self, key: str, attr) -> AttrValue:
		if key == "indices_data":
			if self._get_extra() is None:
				return NodeDefGenerator.get_content_as_compressed_bytearray(attr, self.dtype.value_n_bits)
			else:
				const_range = self._get_extra().to_attr()["indices_range"]
				return NodeDefGenerator.get_content_in_correct_type(const_range)
		elif key == "float_data":
			if self._get_extra() is None:
				return NodeDefGenerator.get_content_in_correct_type(attr)
			else:
				const_range = self._get_extra().to_attr()["float_range"]
				return NodeDefGenerator.get_content_in_correct_type(const_range)
		elif key == "out_dtypes":
			return NodeDefGenerator.get_content_in_correct_type(attr[0])
		else:
			return NodeDefGenerator.get_content_in_correct_type(attr)

	def _after_matching(self):
		self._set_extra(None)

	def _rename_key(self, key) -> str:
		if key in ["outDtypes", "out_dtypes"]:
			return "dtype"
		else:
			return key


