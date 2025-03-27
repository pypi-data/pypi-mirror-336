import unittest
import funcnodes_images as fnimg
from funcnodes_images.imagecontainer import IMAGE_FORMATS
import numpy as np


class Test_IMAGE_FORMATS(unittest.TestCase):
    def test_image_formats(self):
        self.assertEqual(
            IMAGE_FORMATS,
            {"np": fnimg.NumpyImageFormat, "img": fnimg.PillowImageFormat},
        )


class TestNumpyImageFormat(unittest.TestCase):
    def test_format_create(self):
        data = np.random.rand(100, 100, 3)
        fmt = fnimg.get_format("np")(data)
        self.assertIsInstance(fmt, fnimg.NumpyImageFormat)

    def test_wrong_shape(self):
        data = np.random.rand(100, 100, 2)
        with self.assertRaises(ValueError):
            _ = fnimg.NumpyImageFormat(data)

    def test_to_uint8(self):
        data = np.random.rand(100, 100, 1)
        data[0, 0, 0] = 1
        data[1, 1, 0] = 0
        fmt = fnimg.NumpyImageFormat(data)

        self.assertIsInstance(fmt.to_uint8(), np.ndarray)
        self.assertEqual(fmt.to_uint8().max(), 255)
        self.assertEqual(fmt.to_uint8().min(), 0)

        data = np.random.rand(100, 100, 1)
        data[0, 0, 0] = 1
        data *= 100
        fmt = fnimg.NumpyImageFormat(data)
        self.assertIsInstance(fmt.to_uint8(), np.ndarray)
        self.assertEqual(fmt.to_uint8().max(), 100)
        self.assertEqual(fmt.to_uint8().min(), 0)

        data = np.random.rand(100, 100, 1)
        data[0, 0, 0] = 1
        data *= 300
        fmt = fnimg.NumpyImageFormat(data)
        self.assertIsInstance(fmt.to_uint8(), np.ndarray)
        self.assertEqual(fmt.to_uint8().max(), 255)
        self.assertEqual(fmt.to_uint8().min(), 0)

    def test_to_rgb_uint8(self):
        data = np.random.rand(100, 100, 1)
        fmt = fnimg.NumpyImageFormat(data)

        self.assertIsInstance(fmt.to_rgb_uint8(), np.ndarray)
        self.assertEqual(fmt.to_rgb_uint8().dtype, np.uint8)
        self.assertEqual(fmt.to_rgb_uint8().shape, (100, 100, 3))
        self.assertLessEqual(fmt.to_rgb_uint8().max(), 255)
        self.assertGreaterEqual(fmt.to_rgb_uint8().min(), 0)

    def test_short(self):
        data = np.random.rand(100, 100)
        fmt = fnimg.NumpyImageFormat(data)

        self.assertIsInstance(fmt, fnimg.NumpyImageFormat)
        self.assertEqual(fmt._data.shape, (100, 100, 1))
