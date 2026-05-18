import h5py
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "data" / "target_run" / "res"
INITIAL = ROOT / "data" / "initial_run" / "res"
MISFIT_DIR = ROOT / "results" / "misfit"
FIG_DIR = ROOT / "results" / "figures"

MISFIT_DIR.mkdir(parents=True, exist_ok=True)
FIG_DIR.mkdir(parents=True, exist_ok=True)

field_name = "press_gll"

target_frames = sorted([p.name for p in TARGET.glob("Rsem*")])
initial_frames = sorted([p.name for p in INITIAL.glob("Rsem*")])
common_frames = sorted(set(target_frames).intersection(initial_frames))

print("Target frames:", len(target_frames))
print("Initial frames:", len(initial_frames))
print("Common frames:", len(common_frames))

rows = []

for frame in common_frames:
    target_path = TARGET / frame / "sem_field.0000.h5"
    initial_path = INITIAL / frame / "sem_field.0000.h5"

    with h5py.File(target_path, "r") as f:
        u_target = f[field_name][:]

    with h5py.File(initial_path, "r") as f:
        u_initial = f[field_name][:]

    diff = u_initial - u_target

    J = 0.5 * np.sum(diff**2)
    rel_l2 = np.linalg.norm(diff) / (np.linalg.norm(u_target) + 1e-30)

    rows.append([
        frame,
        J,
        rel_l2,
        u_target.min(),
        u_target.max(),
        u_initial.min(),
        u_initial.max(),
        diff.min(),
        diff.max(),
    ])

    print(frame, "J =", J, "rel_l2 =", rel_l2)

out_csv = MISFIT_DIR / f"all_snapshot_misfit_{field_name}.csv"

with open(out_csv, "w") as f:
    f.write("frame,J,relative_l2,target_min,target_max,initial_min,initial_max,diff_min,diff_max\n")
    for row in rows:
        f.write(",".join([str(v) for v in row]) + "\n")

frames = [r[0] for r in rows]
J_values = np.array([r[1] for r in rows], dtype=float)
rel_values = np.array([r[2] for r in rows], dtype=float)

best_idx = int(np.argmax(rel_values))
print()
print("=" * 80)
print("Largest relative L2 frame:")
print("Frame:", frames[best_idx])
print("Relative L2:", rel_values[best_idx])
print("J:", J_values[best_idx])
print("CSV saved:", out_csv)

plt.figure(figsize=(8, 4))
plt.plot(range(1, len(frames) + 1), rel_values, marker="o")
plt.xlabel("Snapshot index")
plt.ylabel("Relative L2 misfit")
plt.title(f"Snapshot misfit over time ({field_name})")
plt.grid(True)
plt.tight_layout()
plt.savefig(FIG_DIR / f"all_snapshot_relative_l2_{field_name}.png", dpi=200)
plt.close()

plt.figure(figsize=(8, 4))
plt.plot(range(1, len(frames) + 1), J_values, marker="o")
plt.xlabel("Snapshot index")
plt.ylabel("Snapshot misfit J")
plt.title(f"Snapshot misfit J over time ({field_name})")
plt.grid(True)
plt.tight_layout()
plt.savefig(FIG_DIR / f"all_snapshot_J_{field_name}.png", dpi=200)
plt.close()

print("Figures saved in:", FIG_DIR)
