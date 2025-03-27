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
from typing import Any, Dict, Union, Iterable

import numpy as np
from sklearn.metrics import precision_score

from fastestimator.trace.meta._per_ds import per_ds
from fastestimator.trace.trace import Trace
from fastestimator.util.data import Data
from fastestimator.util.traceability_util import traceable
from fastestimator.util.util import to_number


@per_ds
@traceable()
class Precision(Trace):
    """Computes precision for a classification task and reports it back to the logger.

    Args:
        true_key: Name of the key that corresponds to ground truth in the batch dictionary.
        pred_key: Name of the key that corresponds to predicted score in the batch dictionary.
        mode: What mode(s) to execute this Trace in. For example, "train", "eval", "test", or "infer". To execute
            regardless of mode, pass None. To execute in all modes except for a particular one, you can pass an argument
            like "!infer" or "!train".
        ds_id: What dataset id(s) to execute this Trace in. To execute regardless of ds_id, pass None. To execute in all
            ds_ids except for a particular one, you can pass an argument like "!ds1".
        output_name: Name of the key to store to the state.
        per_ds: Whether to automatically compute this metric individually for every ds_id it runs on, in addition to
            computing an aggregate across all ds_ids on which it runs. This is automatically False if `output_name`
            contains a "|" character.
        **kwargs: Additional keyword arguments that pass to sklearn.metrics.precision_score()

    Raises:
        ValueError: One of ["y_true", "y_pred", "average"] argument exists in `kwargs`.
    """
    def __init__(self,
                 true_key: str,
                 pred_key: str,
                 mode: Union[None, str, Iterable[str]] = ("eval", "test"),
                 ds_id: Union[None, str, Iterable[str]] = None,
                 output_name: str = "precision",
                 per_ds: bool = True,
                 **kwargs) -> None:
        Precision.check_kwargs(kwargs)
        super().__init__(inputs=(true_key, pred_key), outputs=output_name, mode=mode, ds_id=ds_id)
        self.binary_classification = None
        self.y_true = []
        self.y_pred = []
        self.kwargs = kwargs
        self.per_ds = per_ds

    @property
    def true_key(self) -> str:
        return self.inputs[0]

    @property
    def pred_key(self) -> str:
        return self.inputs[1]

    def on_epoch_begin(self, data: Data) -> None:
        self.y_true = []
        self.y_pred = []

    def on_batch_end(self, data: Data) -> None:
        y_true, y_pred = to_number(data[self.true_key]), to_number(data[self.pred_key])
        self.binary_classification = y_pred.shape[-1] == 1
        if y_true.shape[-1] > 1 and y_true.ndim > 1:
            y_true = np.argmax(y_true, axis=-1)
        if y_pred.shape[-1] > 1 and y_pred.ndim > 1:
            y_pred = np.argmax(y_pred, axis=-1)
        else:
            y_pred = np.round(y_pred)
        assert y_pred.size == y_true.size
        self.y_pred.extend(y_pred.ravel())
        self.y_true.extend(y_true.ravel())

    def on_epoch_end(self, data: Data) -> None:
        if self.binary_classification:
            score = precision_score(self.y_true, self.y_pred, average='binary', **self.kwargs)
        else:
            score = precision_score(self.y_true, self.y_pred, average=None, **self.kwargs)
        data.write_with_log(self.outputs[0], score)

    @staticmethod
    def check_kwargs(kwargs: Dict[str, Any]) -> None:
        """Check if `kwargs` has any blacklist argument and raise an error if it does.

        Args:
            kwargs: Keywork arguments to be examined.

        Raises:
            ValueError: One of ["y_true", "y_pred", "average"] argument exists in `kwargs`.
        """
        blacklist = ["y_true", "y_pred", "average"]
        illegal_kwarg = [x for x in blacklist if x in kwargs]
        if illegal_kwarg:
            raise ValueError(
                f"Arguments {illegal_kwarg} cannot exist in kwargs, since FastEstimator will later directly use them in"
                " sklearn.metrics.precision_score()")
