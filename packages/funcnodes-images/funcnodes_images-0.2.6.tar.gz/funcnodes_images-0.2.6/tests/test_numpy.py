import unittest
from funcnodes_images._numpy import NumpyImageFormat
import numpy as np


class TestNumpyImageFormat(unittest.TestCase):
    def test_initialization(self):
        arr = np.zeros((10, 10, 3))
        img_format = NumpyImageFormat(arr)
        self.assertIsInstance(img_format, NumpyImageFormat)

    def test_bad_initialization(self):
        with self.assertRaises(ValueError):
            NumpyImageFormat(np.zeros((10, 10, 2)))  # 2 channels

    def test_to_uint8(self):
        arr = np.random.rand(10, 10, 3) * 300  # values greater than 255
        img_format = NumpyImageFormat(arr)
        uint8_array = img_format.to_uint8()
        self.assertTrue(np.all(uint8_array <= 255))
        self.assertTrue(np.all(uint8_array >= 0))
        self.assertEqual(uint8_array.dtype, np.uint8)


# Additional tests for dimension expansion, channel checks, etc.
