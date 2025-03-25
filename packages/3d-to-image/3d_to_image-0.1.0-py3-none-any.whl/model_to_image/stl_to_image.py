import io
import matplotlib.pyplot as plt
import trimesh
from typing import Dict, Optional

def process_stl(file_path: str) -> Dict[str, Optional[bytes]]:
    def plot_mesh(mesh, azim, elev) -> Optional[io.BytesIO]:
        try:
            fig = plt.figure(figsize=(8, 8))
            ax = fig.add_subplot(111, projection='3d')
            ax.set_box_aspect([1, 1, 1])
            ax.plot_trisurf(
                mesh.vertices[:, 0],
                mesh.vertices[:, 1],
                triangles=mesh.faces,
                Z=mesh.vertices[:, 2],
                color=(0.5, 0.5, 0.5, 0.7),
                edgecolor='k',
                linewidth=0.2
            )
            ax.view_init(elev=elev, azim=azim)
            ax.axis('off')

            buf = io.BytesIO()
            plt.savefig(buf, format='png', bbox_inches='tight')
            plt.close(fig)

            buf.seek(0)
            return buf
        except Exception:
            plt.close('all')
            return Exception

    try:
        mesh = trimesh.load_mesh(file_path)
        if not isinstance(mesh, trimesh.Trimesh):
            raise ValueError("Invalid mesh format")

        views = {"front": (0, 0), "back": (180, 0), "left": (90, 0), "right": (-90, 0)}
        view_buffers = {view: plot_mesh(mesh, azim, elev) for view, (azim, elev) in views.items()}
        return {view: buf.getvalue() if buf else None for view, buf in view_buffers.items()}
    except Exception as e:
        return {"error": f"Failed to process .stl file: {str(e)}"}
