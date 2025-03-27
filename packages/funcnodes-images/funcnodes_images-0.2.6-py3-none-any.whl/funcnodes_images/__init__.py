from .imagecontainer import register_imageformat, get_format, ImageFormat
from ._numpy import NumpyImageFormat
from ._pillow import PillowImageFormat
import funcnodes as fn
from exposedfunctionality.function_parser.types import add_type
from . import image_nodes as nodes
import funcnodes_numpy as fn_numpy  # noqa: F401 # import for type hinting

add_type(ImageFormat, "ImageFormat")

FUNCNODES_RENDER_OPTIONS: fn.RenderOptions = {
    "typemap": {
        ImageFormat: "image",
    },
}


def imageFormatEncoder(obj: ImageFormat, preview=False):
    if isinstance(obj, ImageFormat):
        if preview:
            return obj.to_thumbnail((200, 200)).to_jpeg(), True
        return obj.to_jpeg(), True
    return obj, False


fn.JSONEncoder.add_encoder(imageFormatEncoder)


def imageFormatbytesEncoder(obj: ImageFormat, preview=False) -> fn.BytesEncdata:
    if isinstance(obj, ImageFormat):
        return fn.BytesEncdata(
            data=(obj.to_thumbnail((200, 200)) if preview else obj).to_jpeg(),
            mime="image/jpeg",
            handeled=True,
        )
    return fn.BytesEncdata(data=obj, handeled=False)


fn.ByteEncoder.add_encoder(imageFormatbytesEncoder, enc_cls=[ImageFormat])

NODE_SHELF = nodes.NODE_SHELF

__all__ = [
    "register_imageformat",
    "NumpyImageFormat",
    "get_format",
    "PillowImageFormat",
    "ImageFormat",
    "nodes",
    "FUNCNODES_RENDER_OPTIONS",
    "NODE_SHELF",
]


__version__ = "0.2.6"
