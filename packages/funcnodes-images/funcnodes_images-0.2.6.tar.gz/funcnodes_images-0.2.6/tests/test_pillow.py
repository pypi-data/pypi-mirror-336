import unittest
from funcnodes_images._pillow import PillowImageFormat
from PIL import Image
import numpy as np


class TestPillowImageFormat(unittest.TestCase):
    def test_initialization(self):
        img = Image.new("RGB", (10, 10))
        img_format = PillowImageFormat(img)
        self.assertIsInstance(img_format, PillowImageFormat)

    def test_to_array(self):
        img = Image.new("RGB", (10, 10))
        img_format = PillowImageFormat(img)
        arr = img_format.to_array()
        self.assertIsInstance(arr, np.ndarray)
        self.assertEqual(arr.shape, (10, 10, 3))


# Additional tests for conversions, error handling on bad input, etc.
