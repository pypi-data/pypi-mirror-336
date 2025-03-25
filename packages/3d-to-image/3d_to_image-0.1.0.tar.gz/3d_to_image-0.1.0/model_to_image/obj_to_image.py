import pyvista as pv
import io
from PIL import Image
from typing import Dict, Optional

def process_obj(file_path) -> Dict[str, Optional[bytes]]:
    try:
        mesh = pv.read(file_path)
        plotter = pv.Plotter(off_screen=True)
        plotter.add_mesh(mesh)
        image_array = plotter.screenshot()
        plotter.close()

        image = Image.fromarray(image_array)
        image_bytes_io = io.BytesIO()
        image.save(image_bytes_io, format='PNG')
        image_bytes_io.seek(0)
        return image_bytes_io
    except Exception as e:
        print(f"Failed to capture screenshot for {file_path}: {e}")
        return None
