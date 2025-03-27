from abc import ABC, abstractmethod
from typing import Type, Optional
import numpy as np
from typing import Any, Generic, TypeVar, Callable, Dict
import io
from PIL import Image
from .utils import calc_new_size, calc_crop_values

from funcnodes_core.config import update_render_options

T = TypeVar("T")


IMAGE_FORMATS: Dict[str, Type["ImageFormat"]] = {}


class ImageFormat(ABC, Generic[T]):  # noqa: F821
    _to_converters: Dict[
        "ImageFormat", Dict["ImageFormat", Callable[["ImageFormat"], "ImageFormat"]]
    ] = {}

    def __init__(self, data: T):
        self._data: T = data

    @property
    def data(self) -> T:
        return self.get_data_copy()

    @abstractmethod
    def get_data_copy(self) -> T:
        pass

    @abstractmethod
    def width(self) -> int:
        pass

    @abstractmethod
    def height(self) -> int:
        pass

    def to(self, cls: Type["ImageFormat"] | str) -> "ImageFormat":
        if isinstance(cls, str):
            cls = IMAGE_FORMATS[cls]
        if self.__class__ == cls:
            return self
        if cls in ImageFormat._to_converters[self.__class__]:
            return self._to_converters[self.__class__][cls](self)

    @classmethod
    def add_to_converter(
        self_cls,
        other_cls: Type["ImageFormat"],
        converter: Callable[["ImageFormat"], "ImageFormat"],
    ):
        if self_cls not in ImageFormat._to_converters:
            ImageFormat._to_converters[self_cls] = {}
        ImageFormat._to_converters[self_cls][other_cls] = converter

    def get_to_converter(
        self, cls: Type["ImageFormat"]
    ) -> Callable[["ImageFormat"], "ImageFormat"]:
        if self.__class__ == cls:
            return lambda x: x
        if self.__class__ not in ImageFormat._to_converters:
            ImageFormat._to_converters[self.__class__] = {}
        return ImageFormat._to_converters[self.__class__].get(cls)

    def __getattribute__(self, name: str) -> Any:
        try:
            return super().__getattribute__(name)
        except AttributeError:
            if name.startswith("to_"):
                _to = name[3:]

                if _to in IMAGE_FORMATS:
                    other = IMAGE_FORMATS[_to]
                    conv = self.get_to_converter(other)
                    if conv:
                        return lambda: conv(self)
            raise

    @classmethod
    def from_array(cls, data: np.ndarray):
        from ._numpy import NumpyImageFormat

        return NumpyImageFormat(data).to(cls)

    def to_array(self) -> np.ndarray:
        return self.to_np().data

    def __array__(self, dtype=None, copy=None):
        arr = self.to_array()
        if dtype:
            arr = arr.astype(dtype)
        if copy is not None and not copy:
            raise ValueError("copy=False is not supported")
        return arr

    @classmethod
    def from_file(cls, path: str):
        from ._pillow import PillowImageFormat

        img = Image.open(path)
        return PillowImageFormat(img).to(cls)

    @classmethod
    def from_bytes(cls, data: bytes):
        from ._pillow import PillowImageFormat

        buff = io.BytesIO(data)
        img = Image.open(buff)
        img.load()
        buff.close()
        return PillowImageFormat(img).to(cls)

    def to_jpeg(self, quality=75) -> bytes:
        img: Image = self.to_img().data
        img = img.convert("RGB")
        img_byte_array = io.BytesIO()
        img.save(img_byte_array, format="JPEG", quality=int(quality))
        return img_byte_array.getvalue()

    def to_png(self) -> bytes:
        img: Image = self.to_img().data
        img = img.convert("RGB")
        img_byte_array = io.BytesIO()
        img.save(img_byte_array, format="PNG")
        return img_byte_array.getvalue()

    def to_thumbnail(self, size: tuple) -> "ImageFormat[T]":
        img: Image = self.to_img().data
        img.thumbnail(size)
        return self.__class__.from_array(np.array(img))

    def resize(
        self,
        w: int = None,
        h: int = None,
    ) -> "ImageFormat[T]":
        img: Image = self.to_img().data
        new_x, new_y = calc_new_size(img.width, img.height, w, h)
        img = img.resize((new_x, new_y))
        return self.__class__.from_array(np.array(img))

    def crop(
        self,
        x1: Optional[int] = None,
        y1: Optional[int] = None,
        x2: Optional[int] = None,
        y2: Optional[int] = None,
    ) -> "ImageFormat[T]":
        img: Image = self.to_img().data
        x1, y1, x2, y2 = calc_crop_values(img.width, img.height, x1, y1, x2, y2)

        img = img.crop((x1, y1, x2, y2))
        return self.__class__.from_array(np.array(img))

    def scale(self, factor: float) -> "ImageFormat[T]":
        if factor <= 0:
            raise ValueError("factor must be greater than 0")

        img: Image = self.to_img().data
        img = img.resize((int(img.width * factor), int(img.height * factor)))
        return self.__class__.from_array(np.array(img))


def register_imageformat(
    imageformat: Type[ImageFormat], key: str, overwrite=False, _raise=True
):
    if not issubclass(imageformat, ImageFormat):
        raise ValueError("format must be a subclass of ImageFormat")
    if key in IMAGE_FORMATS:
        if IMAGE_FORMATS[key] == imageformat:
            return
        if not overwrite:
            if _raise:
                raise ValueError(
                    f"key '{key} 'already exists in image_formats as {IMAGE_FORMATS[key]}"
                )
            else:
                return
    IMAGE_FORMATS[key] = imageformat

    update_render_options(
        {
            "typemap": {
                imageformat: "image",
            }
        }
    )


def get_format(key: str) -> Type[ImageFormat]:
    return IMAGE_FORMATS[key]
