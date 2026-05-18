import h5py
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "data" / "target_run"
INITIAL = ROOT / "data" / "initial_run"
FIG_DIR = ROOT / "results" / "figures"
MISFIT_DIR = ROOT / "results" / "misfit"

FIG_DIR.mkdir(parents=True, exist_ok=True)
MISFIT_DIR.mkdir(parents=True, exist_ok=True)

frame = "Rsem0010"
field_name = "press_gll"

target_field_path = TARGET / "res" / frame / "sem_field.0000.h5"
initial_field_path = INITIAL / "res" / frame / "sem_field.0000.h5"

target_geom_path = TARGET / "res" / "geometry0000.h5"
initial_geom_path = INITIAL / "res" / "geometry0000.h5"

with h5py.File(target_geom_path, "r") as f:
    nodes_t = f["Nodes"][:]
    lamb_t = f["Lamb"][:]
    mu_t = f["Mu"][:]

with h5py.File(initial_geom_path, "r") as f:
    nodes_i = f["Nodes"][:]
    lamb_i = f["Lamb"][:]
    mu_i = f["Mu"][:]

print("Target nodes:", nodes_t.shape)
print("Initial nodes:", nodes_i.shape)

if nodes_t.shape != nodes_i.shape:
    raise RuntimeError(f"Node shapes differ: {nodes_t.shape} vs {nodes_i.shape}")

node_error = np.max(np.abs(nodes_t - nodes_i))
print("Max node coordinate difference:", node_error)

with h5py.File(target_field_path, "r") as f:
    u_target = f[field_name][:]

with h5py.File(initial_field_path, "r") as f:
    u_initial = f[field_name][:]

diff = u_initial - u_target

J = 0.5 * np.sum(diff**2)
rel_l2 = np.linalg.norm(diff) / (np.linalg.norm(u_target) + 1e-30)

print()
print("=" * 80)
print("Snapshot comparison")
print("Frame:", frame)
print("Field:", field_name)
print("Target min/max:", u_target.min(), u_target.max())
print("Initial min/max:", u_initial.min(), u_initial.max())
print("Diff min/max:", diff.min(), diff.max())
print("Snapshot misfit J:", J)
print("Relative L2:", rel_l2)

out_csv = MISFIT_DIR / f"snapshot_misfit_{frame}_{field_name}.csv"
np.savetxt(
    out_csv,
    np.array([[J, rel_l2, u_target.min(), u_target.max(), u_initial.min(), u_initial.max(), diff.min(), diff.max()]]),
    delimiter=",",
    header="J,relative_l2,target_min,target_max,initial_min,initial_max,diff_min,diff_max",
    comments=""
)

x = nodes_t[:, 0]
y = nodes_t[:, 1]
z = nodes_t[:, 2]

mask = np.abs(y) < 0.25
if mask.sum() < 100:
    mask = np.abs(y) < 1.5
if mask.sum() < 100:
    mask = np.abs(y) < 3.0

print("Section points for plotting:", mask.sum())

def scatter_section(values, title, filename):
    plt.figure(figsize=(7, 5))
    sc = plt.scatter(x[mask], z[mask], c=values[mask], s=1)
    plt.colorbar(sc)
    plt.xlabel("x (m)")
    plt.ylabel("z (m)")
    plt.title(title)
    plt.tight_layout()
    plt.savefig(FIG_DIR / filename, dpi=200)
    plt.close()

scatter_section(
    u_target,
    f"Target {field_name}, {frame}, y≈0",
    f"target_{field_name}_{frame}_xz.png",
)

scatter_section(
    u_initial,
    f"Initial {field_name}, {frame}, y≈0",
    f"initial_{field_name}_{frame}_xz.png",
)

scatter_section(
    diff,
    f"Initial - Target {field_name}, {frame}, y≈0",
    f"diff_{field_name}_{frame}_xz.png",
)

scatter_section(
    lamb_t - lamb_i,
    "Target - Initial lambda, y≈0",
    "lambda_target_minus_initial_xz.png",
)

scatter_section(
    mu_t - mu_i,
    "Target - Initial mu, y≈0",
    "mu_target_minus_initial_xz.png",
)

print()
print("Saved figures in:", FIG_DIR)
print("Saved misfit CSV:", out_csv)
