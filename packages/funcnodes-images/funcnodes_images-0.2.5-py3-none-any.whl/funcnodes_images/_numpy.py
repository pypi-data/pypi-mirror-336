from .imagecontainer import ImageFormat, register_imageformat


import numpy as np


class NumpyImageFormat(ImageFormat[np.ndarray]):
    def __init__(self, arr: np.ndarray) -> None:
        # check if arr is a numpy array
        if not isinstance(arr, np.ndarray):
            raise TypeError("arr must be a numpy array")
        # make shure arr has 3 dimensions or fail

        if len(arr.shape) != 3:
            if len(arr.shape) == 2:
                arr = np.expand_dims(arr, axis=2)
            else:
                raise ValueError("arr must have 3 dimensions")

        # allow 3 or 1 channel images
        if arr.shape[2] != 3 and arr.shape[2] != 1 and arr.shape[2] != 4:
            raise ValueError(
                f"arr must have 1,3 or 4 channels but has shape {arr.shape}"
            )

        super().__init__(arr)

    def get_data_copy(self) -> np.ndarray:
        return self._data.copy()

    def width(self) -> int:
        return self._data.shape[1]

    def height(self) -> int:
        return self._data.shape[0]

    def to_uint8(self) -> np.ndarray:
        d = self.data
        if d.dtype == np.uint8:
            return d

        _max = d.max()
        _min = d.min()

        # if in range 0-255
        if _max <= 255 and _min >= 0 and _max > 1:
            return d.astype(np.uint8)

        # if not in range 0-1 -> normalize
        if _max > 1 or _min < 0:
            d = d - _min
            if _max != _min:
                d = d / (_max - _min)

        return (d * 255).astype(np.uint8)

    def to_rgb_or_rgba_uint8(self) -> np.ndarray:
        d = self.to_uint8()
        if d.shape[2] == 3 or d.shape[2] == 4:
            return d

        return np.repeat(d, 3, axis=2)

    def to_rgb_uint8(self) -> np.ndarray:
        d = self.to_uint8()
        if d.shape[2] == 3:
            return d

        if d.shape[2] == 4:
            return d[:, :, :3]

        return np.repeat(d, 3, axis=2)

    def to_rgba_uint8(self) -> np.ndarray:
        d = self.to_uint8()
        if d.shape[2] == 4:
            return d

        if d.shape[2] == 3:
            return np.concatenate(
                [d, np.full(d.shape[:2] + (1,), 255, dtype=np.uint8)], axis=2
            )

        return np.repeat(d, 4, axis=2)

    def to_array(self) -> np.ndarray:
        return self.get_data_copy()


register_imageformat(NumpyImageFormat, "np")
