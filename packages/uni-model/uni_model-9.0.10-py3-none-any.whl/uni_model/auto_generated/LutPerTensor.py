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
from uni_model.auto_generated.Lut import Lut
from uni_model.auto_generated.Qtype import Qtype
from uni_model.auto_generated.Dtype import Dtype
from typing import List
from uni_model.model.accuracy.min_max import MinMaxOpenEnded


@dataclass(frozen=True)
class LutPerTensor(Lut, Qtype, Dtype):
	value_n_bits: int # Number of bits that determines the quantization range, usually 8
	table: List[float] 
	table_n_bits: int # size of lut, usually 2 or 4
	min_max: MinMaxOpenEnded 

	def __eq__(self, other):
		if self.value_n_bits != other.value_n_bits or not np.allclose(self.table, other.table) or self.table_n_bits != other.table_n_bits or self.min_max != other.min_max:
			return False
		return True

	def __hash__(self):
		return hash((self.value_n_bits, tuple(np.array(self.table, dtype='float32')), self.table_n_bits, self.min_max))


