# Copyright 2021 The FastEstimator Authors. All Rights Reserved.
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
import random
from typing import Any, Dict, Iterable, List, Union

import numpy as np
from PIL import Image, ImageTransform

from fastestimator.op.numpyop.numpyop import NumpyOp
from fastestimator.util.traceability_util import traceable
from fastestimator.util.base_util import param_to_range


@traceable()
class ShearY(NumpyOp):
    """Randomly shear the image along the Y axis.

    This is a wrapper for functionality provided by the PIL library:
    https://github.com/python-pillow/Pillow/tree/master/src/PIL.

    Args:
        inputs: Key(s) of images to be modified.
        outputs: Key(s) into which to write the modified images.
        mode: What mode(s) to execute this Op in. For example, "train", "eval", "test", or "infer". To execute
            regardless of mode, pass None. To execute in all modes except for a particular one, you can pass an argument
            like "!infer" or "!train".
        ds_id: What dataset id(s) to execute this Op in. To execute regardless of ds_id, pass None. To execute in all
            ds_ids except for a particular one, you can pass an argument like "!ds1".
        shear_coef: Factor range for shear. If shear_coef is a single float, the range will be (-shear_coef, shear_coef)

    Image types:
        uint8
    """
    def __init__(self,
                 inputs: Union[str, Iterable[str]],
                 outputs: Union[str, Iterable[str]],
                 mode: Union[None, str, Iterable[str]] = None,
                 ds_id: Union[None, str, Iterable[str]] = None,
                 shear_coef: float = 0.3):
        super().__init__(inputs=inputs, outputs=outputs, mode=mode, ds_id=ds_id)
        self.shear_coef = param_to_range(shear_coef)
        self.in_list, self.out_list = True, True

    def set_rua_level(self, magnitude_coef: float) -> None:
        """Set the augmentation intensity based on the magnitude_coef.

        This method is specifically designed to be invoked by the RUA Op.

        Args:
            magnitude_coef: The desired augmentation intensity (range [0-1]).
        """
        param_mid = (self.shear_coef[1] + self.shear_coef[0]) / 2
        param_extent = magnitude_coef * ((self.shear_coef[1] - self.shear_coef[0]) / 2)
        self.shear_coef = (param_mid - param_extent, param_mid + param_extent)

    def forward(self, data: List[np.ndarray], state: Dict[str, Any]) -> List[np.ndarray]:
        shear_coeff = random.uniform(self.shear_coef[0], self.shear_coef[1])
        return [ShearY._apply_sheary(elem, shear_coeff) for elem in data]

    @staticmethod
    def _apply_sheary(data: np.ndarray, shear_coeff: float) -> np.ndarray:
        im = Image.fromarray(data)
        width, height = im.size
        yshift = round(abs(shear_coeff) * height)
        newheight = height + yshift
        im = im.transform((width, newheight),
                          ImageTransform.AffineTransform(
                              (1.0, 0.0, 0.0, shear_coeff, 1.0, -yshift if shear_coeff > 0 else 0.0)),
                          resample=Image.BICUBIC)
        im = im.resize((width, height))
        return np.array(im)
