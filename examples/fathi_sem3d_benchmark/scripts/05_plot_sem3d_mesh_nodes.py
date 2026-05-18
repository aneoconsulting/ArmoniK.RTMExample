import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data" / "processed"
FIG_DIR = ROOT / "results" / "figures"
FIG_DIR.mkdir(parents=True, exist_ok=True)

nodes_path = DATA_DIR / "sem3d_mesh_local_nodes_target.npy"
nodes = np.load(nodes_path)

x = nodes[:, 0]
y = nodes[:, 1]
z = nodes[:, 2]

print("Number of unique mesh nodes:", len(nodes))
print("x range:", x.min(), x.max())
print("y range:", y.min(), y.max())
print("z range:", z.min(), z.max())

plt.figure(figsize=(7, 6))
plt.scatter(x, z, s=2)
plt.xlabel("x (m)")
plt.ylabel("z (m)")
plt.title("SEM3D mesh local nodes: x-z projection")
plt.grid(True)
plt.tight_layout()
plt.savefig(FIG_DIR / "sem3d_mesh_nodes_xz_preview.png", dpi=200)

plt.figure(figsize=(7, 6))
plt.scatter(x, y, s=2)
plt.xlabel("x (m)")
plt.ylabel("y (m)")
plt.title("SEM3D mesh local nodes: x-y projection")
plt.grid(True)
plt.axis("equal")
plt.tight_layout()
plt.savefig(FIG_DIR / "sem3d_mesh_nodes_xy_preview.png", dpi=200)

print("Figures saved:")
print(FIG_DIR / "sem3d_mesh_nodes_xz_preview.png")
print(FIG_DIR / "sem3d_mesh_nodes_xy_preview.png")
