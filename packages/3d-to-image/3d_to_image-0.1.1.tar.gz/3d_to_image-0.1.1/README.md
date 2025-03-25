# model-to-image

[![PyPI version](https://badge.fury.io/py/3d-to-image.svg)](https://badge.fury.io/py/3d-to-image)

`model-to-image` is a Python package that converts 3D models (OBJ, GLB, and STL) into 2D images. It leverages libraries like `pyrender`, `pyvista`, `trimesh`, and `matplotlib` to render and capture images from different viewpoints.  This is useful for generating previews, thumbnails, or for use in applications where 3D rendering is not feasible.

## Features

*   **OBJ to Image:** Converts `.obj` files to PNG images using `pyvista`.
*   **GLB to Image:** Converts `.glb` files to PNG images using `pyrender`.  Handles scene setup, camera positioning, and lighting automatically.  Uses EGL on Linux for offscreen rendering.
*   **STL to Images (Multiple Views):** Converts `.stl` files to multiple PNG images, capturing "front", "back", "left", and "right" views using `matplotlib`.
*   **Error Handling:** Includes robust error handling to catch and report issues during file processing.  Returns informative error messages.
*   **In-Memory Operations:**  Primarily uses in-memory `io.BytesIO` objects for efficient image handling, avoiding unnecessary disk I/O.
*   **Dependencies automatically installed:** Includes `pyrender`, `trimesh`, `pyvista`, `matplotlib`, `Pillow` and the rest of the requirements.

## Installation

```bash
pip install 3d-to-image
```

On Linux, the pyrender portion (GLB conversion) requires an EGL-capable system. If you encounter issues, ensure you have the necessary EGL drivers installed. You may also need to install additional system packages like libgl1-mesa-dev and libegl1-mesa-dev (on Debian/Ubuntu):

```bash
sudo apt-get update  # or your distribution's equivalent
sudo apt-get install libgl1-mesa-dev libegl1-mesa-dev
```

If you encounter an error involving OSError and OSMesa, install:

```bash
sudo apt-get install libosmesa6-dev
```
And set the following environment variable prior to running:

```bash
export PYOPENGL_PLATFORM=osmesa
```

## Usage

The package provides three main functions: process_obj, glb_to_image, and process_stl.

```python
from model_to_image import process_obj, glb_to_image, process_stl
import io

# --- OBJ to Image ---
obj_image_bytes = process_obj("path/to/your/model.obj")  # Returns a BytesIO object
if obj_image_bytes:
    with open("output_obj.png", "wb") as f:
        f.write(obj_image_bytes.getvalue())
    print("OBJ image saved.")
else:
	print("OBJ conversion failed.")


# --- GLB to Image ---
with open("path/to/your/model.glb", "rb") as f:
    glb_bytes = f.read()

glb_image_bytes = glb_to_image(glb_bytes)  # Returns a BytesIO object or an error string

if isinstance(glb_image_bytes, io.BytesIO):
    with open("output_glb.png", "wb") as f:
        f.write(glb_image_bytes.getvalue())
    print("GLB image saved.")
else:
    print(glb_image_bytes) # Print the error message


# --- STL to Multiple Images ---
stl_images = process_stl("path/to/your/model.stl") # Returns a dictionary of BytesIO objects
if "error" in stl_images:
   print(stl_images["error"])
else:
    for view, img_bytes in stl_images.items():
        if img_bytes:  # Check if img_bytes is not None
            with open(f"output_stl_{view}.png", "wb") as f:
                f.write(img_bytes)
            print(f"STL {view} image saved.")
```

## Explanation:

Import: Import the necessary functions from the model_to_image package.

### process_obj:

Takes the path to an OBJ file as input.

Returns an io.BytesIO object containing the PNG image data, or None on failure.

### glb_to_image:

Takes the GLB file content as bytes (file_bytes) as input.

Returns an io.BytesIO object containing the PNG image data, or a string describing the error on failure.

### process_stl:

Takes the path to an STL file as input.

Returns a dictionary. The keys are view names ("front", "back", "left", "right"), and the values are io.BytesIO objects containing the PNG image data for each view, or None if a view failed. If the entire process failed, it returns a dictionary with an "error" key containing the error message.

Saving Images: The example code demonstrates how to save the image data from the BytesIO objects to files. The key improvement here is the use of .getvalue() to get the bytes from the BytesIO object before writing to the file.

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## License

This project is licensed under the Creative Commons Attribution-NoDerivatives (CC BY-ND) License.