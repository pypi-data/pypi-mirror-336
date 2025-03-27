# Copyright 2023 The FastEstimator Authors. All Rights Reserved.
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
import unittest

import numpy as np

from fastestimator.op.numpyop.univariate import FDA


class TestFDA(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.single_input = [np.random.rand(28, 28, 3)]
        cls.single_output_shape = (28, 28, 3)

        cls.ref_image_single = [np.random.rand(28, 28, 3)]
        cls.ref_image_multiple = [np.random.rand(28, 28, 3), np.random.rand(28, 28, 3), np.random.rand(28, 28, 3)]

    def test_single_input(self):
        fda = FDA(inputs='x', outputs='x', reference_images=self.ref_image_single)
        output = fda.forward(data=self.single_input, state={})
        with self.subTest('Check output type'):
            self.assertEqual(type(output), list)
        with self.subTest('Check output image shape'):
            self.assertEqual(output[0].shape, self.single_output_shape)


    def test_input_image_and_mask(self):
        fda = FDA(inputs='x', outputs='x', reference_images=self.ref_image_multiple)
        output = fda.forward(data=self.single_input, state={})
        with self.subTest('Check output type'):
            self.assertEqual(type(output), list)
        with self.subTest('Check output image shape'):
            self.assertEqual(output[0].shape, self.single_output_shape)