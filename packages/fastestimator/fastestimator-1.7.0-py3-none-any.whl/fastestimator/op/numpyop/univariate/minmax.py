# Copyright 2019 The FastEstimator Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
from typing import Any, Dict, Iterable, List, Union

import numpy as np

from fastestimator.op.numpyop.numpyop import NumpyOp
from fastestimator.util.traceability_util import traceable


@traceable()
class Minmax(NumpyOp):
    """Normalize data using the minmax method.

    Args:
        inputs: Key(s) of images to be modified.
        outputs: Key(s) into which to write the modified images.
        mode: What mode(s) to execute this Op in. For example, "train", "eval", "test", or "infer". To execute
            regardless of mode, pass None. To execute in all modes except for a particular one, you can pass an argument
            like "!infer" or "!train".
        ds_id: What dataset id(s) to execute this Op in. To execute regardless of ds_id, pass None. To execute in all
            ds_ids except for a particular one, you can pass an argument like "!ds1".
        epsilon: A small value to prevent numeric instability in the division.
        new_min: The desired minimum value after the minmax operation.
        new_max: The desired maximum value after the minmax operation.
    """
    def __init__(self,
                 inputs: Union[str, Iterable[str]],
                 outputs: Union[str, Iterable[str]],
                 mode: Union[None, str, Iterable[str]] = None,
                 ds_id: Union[None, str, Iterable[str]] = None,
                 epsilon: float = 1e-7,
                 new_min: float = 0.0,
                 new_max: float = 1.0):
        super().__init__(inputs=inputs, outputs=outputs, mode=mode, ds_id=ds_id)
        self.epsilon = epsilon
        self.new_min = new_min
        self.new_max = new_max
        self.in_list, self.out_list = True, True
        assert new_max > new_min, "the new_max should be greater than new_min."

    def forward(self, data: List[np.ndarray], state: Dict[str, Any]) -> List[np.ndarray]:
        return [self._apply_minmax(elem) for elem in data]

    def _apply_minmax(self, data: np.ndarray) -> np.ndarray:
        data_max = np.max(data)
        data_min = np.min(data)
        data_rescaled = (data - data_min) / max((data_max - data_min), self.epsilon)
        data = data_rescaled * (self.new_max - self.new_min) + self.new_min
        return data.astype(np.float32)
