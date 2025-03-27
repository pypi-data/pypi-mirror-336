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
import inspect
from typing import Any, Dict, List, Union

import numpy as np

from fastestimator.op.numpyop.numpyop import Batch, NumpyOp
from fastestimator.types import FilteredData
from fastestimator.util.traceability_util import traceable


@traceable()
class Sometimes(NumpyOp):
    """Perform a NumpyOp with a given probability.

    Note that Sometimes should not be used to wrap an op whose output key(s) do not already exist in the data
    dictionary. This would result in a problem when future ops / traces attempt to reference the output key, but
    Sometimes declined to generate it. If you want to create a default value for a new key, simply use a LambdaOp before
    invoking the Sometimes.

    Args:
        numpy_op: The operator to be performed.
        prob: The probability of execution, which should be in the range: [0-1).
    """
    def __init__(self, numpy_op: NumpyOp, prob: float = 0.5) -> None:
        # We're going to try to collect any missing output keys from the data dictionary so that they don't get
        # overridden when Sometimes chooses not to execute.
        inps = set(numpy_op.inputs)
        outs = set(numpy_op.outputs)
        self.extra_inputs = list(outs - inps)  # Used by traceability
        self.inp_idx = len(numpy_op.inputs)
        super().__init__(inputs=numpy_op.inputs + self.extra_inputs,
                         outputs=numpy_op.outputs,
                         mode=numpy_op.mode,
                         ds_id=numpy_op.ds_id)
        # Note that in_list and out_list will always be true
        self.op = numpy_op
        if isinstance(numpy_op, Batch):
            raise ValueError("Cannot nest a Batch op inside of Sometimes")
        self.prob = prob

    def __getstate__(self) -> Dict[str, Dict[Any, Any]]:
        return {'op': self.op.__getstate__() if hasattr(self.op, '__getstate__') else {}}

    def set_rua_level(self, magnitude_coef: float) -> None:
        """Set the augmentation intensity based on the magnitude_coef.

        This method is specifically designed to be invoked by the RUA Op.

        Args:
            magnitude_coef: The desired augmentation intensity (range [0-1]).

        Raises:
            AttributeError: If the 'op' doesn't have a 'set_rua_level' method.
        """
        if hasattr(self.op, "set_rua_level") and inspect.ismethod(getattr(self.op, "set_rua_level")):
            self.op.set_rua_level(magnitude_coef=magnitude_coef)
        else:
            raise AttributeError(
                "RUA Augmentations should have a 'set_rua_level' method but it's not present in Op: {}".format(
                    self.op.__class__.__name__))

    def forward(self, data: List[np.ndarray], state: Dict[str, Any]) -> Union[FilteredData, List[np.ndarray]]:
        """Execute the wrapped operator a certain fraction of the time.

        Args:
            data: The information to be passed to the wrapped operator.
            state: Information about the current execution context, for example {"mode": "train"}.

        Returns:
            The original `data`, or the `data` after running it through the wrapped operator.
        """
        if self.prob > np.random.uniform():
            data = data[:self.inp_idx]  # Cut off the unnecessary inputs
            if not self.op.in_list:
                data = data[0]
            data = self.op.forward(data, state)
            if isinstance(data, FilteredData):
                return data
            if not self.op.out_list:
                data = [data]
        else:
            data = [data[self.inputs.index(out)] for out in self.outputs]
        return data

    def forward_batch(self, data: Union[np.ndarray, List[np.ndarray]],
                      state: Dict[str, Any]) -> Union[FilteredData, List[np.ndarray]]:
        if self.prob > np.random.uniform():
            data = data[:self.inp_idx]  # Cut off the unnecessary inputs
            if not self.op.in_list:
                data = data[0]
            data = self.op.forward_batch(data, state)
            if isinstance(data, FilteredData):
                return data
            if not self.op.out_list:
                data = [data]
        else:
            data = [data[self.inputs.index(out)] for out in self.outputs]
        return data
