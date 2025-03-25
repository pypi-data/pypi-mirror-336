import io, os, pyrender, trimesh, sys
import numpy as np
from PIL import Image
from typing import Dict, Optional

def glb_to_image(file_bytes, width=800, height=600) -> Dict[str, Optional[bytes]]:
    try:
        if sys.platform.startswith('linux'):
            # Set the environment variable for PyOpenGL to use EGL for Linux
            os.environ["PYOPENGL_PLATFORM"] = "egl"

        trimesh_scene = trimesh.load(io.BytesIO(file_bytes), file_type='glb')
        scene = pyrender.Scene.from_trimesh_scene(trimesh_scene)

        bbox = trimesh_scene.bounds
        center = (bbox[0] + bbox[1]) / 2
        size = np.linalg.norm(bbox[1] - bbox[0])

        camera = pyrender.PerspectiveCamera(yfov=np.pi / 3.0)
        camera_pose = np.eye(4)
        camera_pose[:3, 3] = center + np.array([0, 0, size * 2])
        scene.add(camera, pose=camera_pose)

        light = pyrender.DirectionalLight(color=np.ones(3), intensity=3.0)
        scene.add(light, pose=camera_pose)

        renderer = pyrender.OffscreenRenderer(width, height)
        color, _ = renderer.render(scene)
        image = Image.fromarray(color)
        renderer.delete()

        output = io.BytesIO()
        image.save(output, format='PNG')
        output.seek(0)

        return output
    except Exception as e:
        return f"Error converting GLB to image: {str(e)}"
