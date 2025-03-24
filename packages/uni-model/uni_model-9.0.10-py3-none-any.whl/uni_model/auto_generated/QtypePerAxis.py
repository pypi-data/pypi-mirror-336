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
from uni_model.auto_generated import Shape
from uni_model.auto_generated.Qtype import Qtype
from uni_model.auto_generated.Dtype import Dtype
from typing import List
from uni_model.model.accuracy.min_max import MinMaxOpenEnded
from uni_model.validation.uni_model_exception import UniModelException


@dataclass(frozen=True)
class QtypePerAxis(Qtype, Dtype):
	value_n_bits: int 
	axis: int 
	min_maxes: List[MinMaxOpenEnded] 

	def validate_shapes(self, shape: Shape):
		size = len(shape.elements)
		dim = self.axis if self.axis >= 0 else size + self.axis
		if dim not in range(size):
			return f"axis {self.axis} is not in the range of shapes {size}"
		if shape.elements[self.axis] == len(self.min_maxes):
			return None
		else:
			return f"shape {shape} in axis {self.axis} doesn't match given min max list with size {len(self.min_maxes)}"

	def __post_init__(self):
		if len(self.min_maxes) == 0:
			raise UniModelException(message="min_maxes mustn't be empty")

	def __hash__(self):
		return hash((self.value_n_bits, self.axis, tuple(self.min_maxes)))


