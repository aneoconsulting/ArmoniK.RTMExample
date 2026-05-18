import h5py
import numpy as np
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUN_DIR = ROOT / "data" / "target_run"

mesh_files = sorted(RUN_DIR.glob("mesh4spec.*.h5"))

if not mesh_files:
    raise FileNotFoundError("No mesh4spec.*.h5 files found.")

all_materials = []

for path in mesh_files:
    with h5py.File(path, "r") as f:
        if "material" not in f:
            print("No material dataset in", path)
            continue

        mat = f["material"][:]
        all_materials.append(mat)

        print()
        print("File:", path.relative_to(ROOT))
        print("material shape:", mat.shape)
        print("unique material ids:", np.unique(mat))
        print("counts:")
        for value in np.unique(mat):
            print("  material", int(value), ":", np.sum(mat == value))

if all_materials:
    all_materials = np.concatenate(all_materials)
    print()
    print("=" * 60)
    print("Global unique material ids:", np.unique(all_materials))
    print("Global counts:")
    for value in np.unique(all_materials):
        print("  material", int(value), ":", np.sum(all_materials == value))
