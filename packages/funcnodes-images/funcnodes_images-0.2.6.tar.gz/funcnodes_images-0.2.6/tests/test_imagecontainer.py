import unittest
from funcnodes_images.imagecontainer import (
    get_format,
)
from funcnodes_images._numpy import NumpyImageFormat
from funcnodes_images._pillow import PillowImageFormat
from PIL import Image
import numpy as np


class TestImageFormat(unittest.TestCase):
    def test_registration(self):
        f = get_format("np")
        self.assertEqual(f, NumpyImageFormat)
        f = get_format("img")
        self.assertEqual(f, PillowImageFormat)

    def test_to_array(self):
        # assuming conversion to NumpyImageFormat is correctly set up
        img = Image.new("RGB", (10, 10))
        pillow_format = PillowImageFormat(img)
        numpy_array = pillow_format.to_array()
        self.assertIsInstance(numpy_array, np.ndarray)

    def test_converter_registration_and_conversion(self):
        img = Image.new("RGB", (10, 10))
        pillow_format = PillowImageFormat(img)
        numpy_format = pillow_format.to("np")
        self.assertIsInstance(numpy_format, NumpyImageFormat)

    def test_to_thumbnail(self):
        img = Image.new("RGB", (100, 50))
        pillow_format = PillowImageFormat(img)
        thumbnail = pillow_format.to_thumbnail((50, 50))
        self.assertIsInstance(thumbnail.data, Image.Image)
        self.assertEqual(thumbnail.data.size, (50, 25))
