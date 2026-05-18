import h5py
import numpy as np
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUN_DIR = ROOT / "data" / "target_run"
OUT_DIR = ROOT / "data" / "processed"
OUT_DIR.mkdir(parents=True, exist_ok=True)

mesh_files = sorted(RUN_DIR.glob("mesh4spec.*.h5"))

print("Mesh files found:")
for p in mesh_files:
    print(" -", p.relative_to(ROOT))

if not mesh_files:
    raise FileNotFoundError("No mesh4spec.*.h5 files found in data/target_run.")

all_nodes = []

for path in mesh_files:
    with h5py.File(path, "r") as f:
        if "local_nodes" not in f:
            print("No local_nodes in", path)
            continue

        nodes = f["local_nodes"][:]
        print()
        print("Reading:", path.relative_to(ROOT))
        print("local_nodes shape:", nodes.shape)
        print("x min/max:", nodes[:, 0].min(), nodes[:, 0].max())
        print("y min/max:", nodes[:, 1].min(), nodes[:, 1].max())
        print("z min/max:", nodes[:, 2].min(), nodes[:, 2].max())

        all_nodes.append(nodes)

if not all_nodes:
    raise RuntimeError("No local_nodes datasets found in mesh files.")

all_nodes = np.vstack(all_nodes)

# Remove duplicate nodes shared between partitions.
# Rounding avoids tiny floating point differences.
rounded = np.round(all_nodes, decimals=10)
unique_nodes = np.unique(rounded, axis=0)

out_npy = OUT_DIR / "sem3d_mesh_local_nodes_target.npy"
out_csv = OUT_DIR / "sem3d_mesh_local_nodes_target_preview.csv"

np.save(out_npy, unique_nodes)

np.savetxt(
    out_csv,
    unique_nodes[: min(5000, len(unique_nodes))],
    delimiter=",",
    header="x,y,z",
    comments="",
)

print()
print("=" * 80)
print("Merged SEM3D mesh local nodes")
print("Raw node count:", all_nodes.shape[0])
print("Unique node count:", unique_nodes.shape[0])
print("Shape:", unique_nodes.shape)
print()
print("x min/max:", unique_nodes[:, 0].min(), unique_nodes[:, 0].max())
print("y min/max:", unique_nodes[:, 1].min(), unique_nodes[:, 1].max())
print("z min/max:", unique_nodes[:, 2].min(), unique_nodes[:, 2].max())
print()
print("Saved full merged nodes to:")
print(out_npy)
print()
print("Saved preview CSV to:")
print(out_csv)
print()
print("Important note:")
print("These nodes come from mesh4spec local_nodes after mesher.")
print("They are useful to inspect the SEM3D mesh geometry.")
print("The final solver output may later contain geometry0000.h5 with full GLL / output nodes.")
