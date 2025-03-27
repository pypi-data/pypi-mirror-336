# FuncNodes Images

## Overview

`funcnodes-images` is an extension of the [FuncNodes](https://github.com/linkdlab/funcnodes) framework that provides nodes for image manipulation and processing. It supports operations like resizing, cropping, and scaling images, and it integrates seamlessly with FuncNodes computational graphs. This package supports image formats such as `PillowImageFormat` and `NumpyImageFormat`, enabling flexibility in handling images via PIL and NumPy.

## Installation

Install the package using:

```bash
pip install funcnodes-images
```

## Getting Started

To begin using `funcnodes-images`, you will need to have the core `FuncNodes` framework installed and set up. Please refer to the [FuncNodes](https://github.com/linkdlab/funcnodes) documentation for details.

### Example Usage

You can integrate the image nodes into your FuncNodes workflows by connecting inputs and outputs between nodes to perform tasks such as resizing, cropping, or converting images between formats.

## Custom Image Formats

This package provides `PillowImageFormat` and `NumpyImageFormat` to handle images using the Pillow and NumPy libraries respectively. You can register your custom image formats by utilizing the `register_imageformat` function.

```python
from funcnodes_images import register_imageformat, ImageFormat

# Custom image format example
class CustomImageFormat(ImageFormat):
    # Define custom format logic here

register_imageformat(CustomImageFormat, 'custom')
```

## Contribution

You are welcome to contribute to this project by submitting pull requests, adding new nodes, fixing bugs, or enhancing the documentation.

## License

This project is licensed under the MIT License.

## Contact

For any questions or issues, please open an issue on the GitHub repository.
