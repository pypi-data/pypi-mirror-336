from all_nodes_test_base import TestAllNodesBase

import funcnodes_images as fnimg
import numpy as np
from PIL import Image
import tempfile
import io


class TestAllNodes(TestAllNodesBase):
    def setUp(self) -> None:
        self.img_arr = np.random.randint(0, 255, (100, 100, 3), dtype=np.uint8)
        self.img = Image.fromarray(self.img_arr)

    async def test_from_bytes(self):
        temp_jpg = tempfile.NamedTemporaryFile(suffix=".jpg")
        temp_jpg.close()
        self.img.save(temp_jpg.name, quality=95)
        with open(temp_jpg.name, "rb") as f:
            jpeg_bytes = f.read()

        refimg = Image.open(temp_jpg.name)

        frombytes = fnimg.nodes.FromBytes()
        frombytes.get_input("data").value = jpeg_bytes
        await frombytes
        img: fnimg.PillowImageFormat = frombytes.get_output("img").value
        self.assertIsInstance(img, fnimg.PillowImageFormat)

        np.testing.assert_equal(img.to_array(), np.array(refimg))

    async def test_resize(self):
        resize = fnimg.nodes.ResizeImage()
        resize.get_input("img").value = fnimg.PillowImageFormat(self.img)
        resize.get_input("width").value = 50
        resize.get_input("height").value = 50

        import asyncio

        await asyncio.sleep(1)
        img: fnimg.PillowImageFormat = resize.get_output("resized_img").value
        self.assertEqual(img.to_array().shape, (50, 50, 3))

    async def test_crop(self):
        crop = fnimg.nodes.CropImage()
        crop.get_input("img").value = fnimg.PillowImageFormat(self.img)
        crop.get_input("x1").value = 10
        crop.get_input("y1").value = 10
        crop.get_input("x2").value = 90
        crop.get_input("y2").value = 90

        await crop
        img: fnimg.PillowImageFormat = crop.get_output("cropped_img").value
        self.assertEqual(img.to_array().shape, (80, 80, 3))

    async def test_scale(self):
        scale = fnimg.nodes.ScaleImage()
        scale.get_input("img").value = fnimg.PillowImageFormat(self.img)
        scale.get_input("scale").value = 0.5

        await scale
        img: fnimg.PillowImageFormat = scale.get_output("scaled_img").value
        self.assertEqual(img.to_array().shape, (50, 50, 3))

    async def test_get_channels_from_rgb(self):
        get_channels = fnimg.nodes.get_channels()
        # testnormal
        get_channels.get_input("img").value = fnimg.PillowImageFormat(self.img)
        await get_channels
        red: fnimg.NumpyImageFormat = get_channels.get_output("red").value
        green: fnimg.NumpyImageFormat = get_channels.get_output("green").value
        blue: fnimg.NumpyImageFormat = get_channels.get_output("blue").value

        self.assertEqual(red.to_array().shape, (100, 100, 1))
        self.assertEqual(green.to_array().shape, (100, 100, 1))
        self.assertEqual(blue.to_array().shape, (100, 100, 1))
        np.testing.assert_equal(red.to_array(), self.img_arr[:, :, [0]])
        np.testing.assert_equal(green.to_array(), self.img_arr[:, :, [1]])
        np.testing.assert_equal(blue.to_array(), self.img_arr[:, :, [2]])

        get_channels.get_input("img").value = fnimg.PillowImageFormat(self.img)
        get_channels.get_input("as_rgb").value = True
        await get_channels
        red: fnimg.NumpyImageFormat = get_channels.get_output("red").value
        green: fnimg.NumpyImageFormat = get_channels.get_output("green").value
        blue: fnimg.NumpyImageFormat = get_channels.get_output("blue").value

        self.assertEqual(red.to_array().shape, (100, 100, 3))
        self.assertEqual(green.to_array().shape, (100, 100, 3))
        self.assertEqual(blue.to_array().shape, (100, 100, 3))

        self.assertTrue(np.all(red.to_array()[:, :, 0] == self.img_arr[:, :, 0]))
        self.assertTrue(np.all(green.to_array()[:, :, 1] == self.img_arr[:, :, 1]))
        self.assertTrue(np.all(blue.to_array()[:, :, 2] == self.img_arr[:, :, 2]))
        self.assertTrue(np.all(red.to_array()[:, :, 1] == 0))
        self.assertTrue(np.all(red.to_array()[:, :, 2] == 0))
        self.assertTrue(np.all(green.to_array()[:, :, 0] == 0))
        self.assertTrue(np.all(green.to_array()[:, :, 2] == 0))
        self.assertTrue(np.all(blue.to_array()[:, :, 0] == 0))
        self.assertTrue(np.all(blue.to_array()[:, :, 1] == 0))

    async def test_get_channels_from_bw(self):
        # bw image
        get_channels = fnimg.nodes.get_channels()
        get_channels.get_input("img").value = fnimg.NumpyImageFormat(
            self.img_arr[:, :, 0]
        )
        await get_channels
        red: fnimg.NumpyImageFormat = get_channels.get_output("red").value
        green: fnimg.NumpyImageFormat = get_channels.get_output("green").value
        blue: fnimg.NumpyImageFormat = get_channels.get_output("blue").value

        self.assertEqual(red.to_array().shape, (100, 100, 1))
        self.assertEqual(green.to_array().shape, (100, 100, 1))
        self.assertEqual(blue.to_array().shape, (100, 100, 1))
        np.testing.assert_equal(red.to_array(), self.img_arr[:, :, [0]])
        np.testing.assert_equal(green.to_array(), self.img_arr[:, :, [0]])
        np.testing.assert_equal(blue.to_array(), self.img_arr[:, :, [0]])

        get_channels.get_input("img").value = fnimg.NumpyImageFormat(
            self.img_arr[:, :, 0]
        )
        get_channels.get_input("as_rgb").value = True
        await get_channels
        red: fnimg.NumpyImageFormat = get_channels.get_output("red").value
        green: fnimg.NumpyImageFormat = get_channels.get_output("green").value
        blue: fnimg.NumpyImageFormat = get_channels.get_output("blue").value

        self.assertEqual(red.to_array().shape, (100, 100, 3))
        self.assertEqual(green.to_array().shape, (100, 100, 3))
        self.assertEqual(blue.to_array().shape, (100, 100, 3))

        np.testing.assert_equal(green.to_array()[:, :, 1], red.to_array()[:, :, 0])
        np.testing.assert_equal(blue.to_array()[:, :, 2], red.to_array()[:, :, 0])
        np.testing.assert_equal(green.to_array()[:, :, 1], blue.to_array()[:, :, 2])

        self.assertTrue(np.all(red.to_array()[:, :, 0] == self.img_arr[:, :, 0]))

        self.assertTrue(np.all(green.to_array()[:, :, 1] == self.img_arr[:, :, 0]))
        self.assertTrue(np.all(blue.to_array()[:, :, 2] == self.img_arr[:, :, 0]))
        self.assertTrue(np.all(red.to_array()[:, :, 1] == 0))
        self.assertTrue(np.all(red.to_array()[:, :, 2] == 0))
        self.assertTrue(np.all(green.to_array()[:, :, 0] == 0))
        self.assertTrue(np.all(green.to_array()[:, :, 2] == 0))
        self.assertTrue(np.all(blue.to_array()[:, :, 0] == 0))
        self.assertTrue(np.all(blue.to_array()[:, :, 1] == 0))

    async def test_get_histograms(self):
        hist = fnimg.nodes.histograms()
        hist.get_input("img").value = fnimg.PillowImageFormat(self.img)
        await hist
        red: np.ndarray = hist.get_output("red").value
        green: np.ndarray = hist.get_output("green").value
        blue: np.ndarray = hist.get_output("blue").value

        self.assertEqual(red.shape, (256,))
        self.assertEqual(green.shape, (256,))
        self.assertEqual(blue.shape, (256,))

        self.assertEqual(red.sum(), 10000)
        self.assertEqual(green.sum(), 10000)
        self.assertEqual(blue.sum(), 10000)

        np.testing.assert_equal(
            red, np.histogram(self.img_arr[:, :, 0], bins=256, range=(0, 255))[0]
        )
        np.testing.assert_equal(
            green, np.histogram(self.img_arr[:, :, 1], bins=256, range=(0, 255))[0]
        )
        np.testing.assert_equal(
            blue, np.histogram(self.img_arr[:, :, 2], bins=256, range=(0, 255))[0]
        )

    async def test_from_array(self):
        fromarray = fnimg.nodes.FromArray()
        fromarray.get_input("data").value = self.img_arr
        await fromarray
        img: fnimg.NumpyImageFormat = fromarray.get_output("img").value
        self.assertEqual(img.to_array().shape, self.img_arr.shape)
        np.testing.assert_equal(img.to_array(), self.img_arr)

    async def test_dimensions(self):
        dim = fnimg.nodes.Dimensions()
        dim.get_input("img").value = fnimg.PillowImageFormat(self.img)
        await dim
        width: int = dim.get_output("width").value
        height: int = dim.get_output("height").value

        self.assertEqual(width, 100)
        self.assertEqual(height, 100)

    async def test_to_array(self):
        toarray = fnimg.nodes.ToArray()
        toarray.get_input("img").value = fnimg.PillowImageFormat(self.img)
        await toarray
        arr: np.ndarray = toarray.get_output("array").value

        self.assertEqual(arr.shape, self.img_arr.shape)
        np.testing.assert_equal(arr, self.img_arr)
        np.testing.assert_equal(np.asarray(self.img), self.img_arr)

    async def test_show_image(self):
        show = fnimg.nodes.ShowImage()
        show.get_input("img").value = fnimg.PillowImageFormat(self.img)
        await show

    async def test_to_jpeg(self):
        tojpeg = fnimg.nodes.to_jpeg()
        tojpeg.get_input("img").value = fnimg.PillowImageFormat(self.img)
        tojpeg.get_input("quality").value = 95
        await tojpeg
        # jpeg: bytes = tojpeg.get_output("jpeg").value

    async def test_to_png(self):
        topng = fnimg.nodes.to_png()
        topng.get_input("img").value = fnimg.PillowImageFormat(self.img)
        await topng
        with Image.open(io.BytesIO(topng["png"].value)) as img:
            self.assertEqual(img.format, "PNG")
