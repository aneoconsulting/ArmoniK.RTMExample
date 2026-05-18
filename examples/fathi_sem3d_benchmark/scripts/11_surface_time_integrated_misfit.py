import h5py
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

TARGET = ROOT / "data" / "target_run" / "res"
INITIAL = ROOT / "data" / "initial_run" / "res"

FIG_DIR = ROOT / "results" / "figures"
MISFIT_DIR = ROOT / "results" / "misfit"

FIG_DIR.mkdir(parents=True, exist_ok=True)
MISFIT_DIR.mkdir(parents=True, exist_ok=True)

# Fields to compare.
# Each field has 3 components: x, y, z
FIELDS = ["displ", "veloc", "accel"]

# Snapshot time interval from input.spec
dt_snapshot = 0.02

# ------------------------------------------------------------
# Read geometry
# ------------------------------------------------------------

with h5py.File(TARGET / "geometry0000.h5", "r") as f:
    nodes_t = f["Nodes"][:]

with h5py.File(INITIAL / "geometry0000.h5", "r") as f:
    nodes_i = f["Nodes"][:]

if nodes_t.shape != nodes_i.shape:
    raise RuntimeError(f"Node shapes differ: {nodes_t.shape} vs {nodes_i.shape}")

node_error = np.max(np.abs(nodes_t - nodes_i))
print("Max node coordinate difference:", node_error)

nodes = nodes_t
x = nodes[:, 0]
y = nodes[:, 1]
z = nodes[:, 2]

# ------------------------------------------------------------
# Select surface nodes
# ------------------------------------------------------------
# Surface is z = 0 in our Fathi-style mesh.
# Because of floating point values and GLL points, use tolerance.

z_surface = z.max()
tol = 1e-5
surface_mask = np.abs(z - z_surface) < tol

if surface_mask.sum() == 0:
    tol = 1e-3
    surface_mask = np.abs(z - z_surface) < tol

if surface_mask.sum() == 0:
    tol = 1e-2
    surface_mask = np.abs(z - z_surface) < tol

print("Surface z:", z_surface)
print("Surface node count:", surface_mask.sum())
print("Total node count:", len(nodes))

surface_indices = np.where(surface_mask)[0]
xs = x[surface_indices]
ys = y[surface_indices]
zs = z[surface_indices]

# ------------------------------------------------------------
# Find common snapshots
# ------------------------------------------------------------

target_frames = sorted([p.name for p in TARGET.glob("Rsem*")])
initial_frames = sorted([p.name for p in INITIAL.glob("Rsem*")])
frames = sorted(set(target_frames).intersection(initial_frames))

print("Target frames:", len(target_frames))
print("Initial frames:", len(initial_frames))
print("Common frames:", len(frames))
print("First/last common frame:", frames[0], frames[-1])

# ------------------------------------------------------------
# Compute time-integrated misfit on surface nodes
# ------------------------------------------------------------

results = {}

for field in FIELDS:
    print()
    print("=" * 80)
    print("Computing field:", field)

    # M(x_surface) = integral ||u_initial - u_target||^2 dt
    misfit_surface = np.zeros(surface_indices.shape[0], dtype=np.float64)

    for frame in frames:
        target_path = TARGET / frame / "sem_field.0000.h5"
        initial_path = INITIAL / frame / "sem_field.0000.h5"

        with h5py.File(target_path, "r") as ft:
            u_t = ft[field][surface_indices, :].astype(np.float64)

        with h5py.File(initial_path, "r") as fi:
            u_i = fi[field][surface_indices, :].astype(np.float64)

        diff = u_i - u_t

        # sum over x/y/z components, then integrate in time
        misfit_surface += np.sum(diff**2, axis=1) * dt_snapshot

    results[field] = misfit_surface

    print("Misfit min/max:", misfit_surface.min(), misfit_surface.max())
    print("Misfit mean:", misfit_surface.mean())
    print("Misfit sum:", misfit_surface.sum())

    out_csv = MISFIT_DIR / f"surface_time_integrated_misfit_{field}.csv"
    np.savetxt(
        out_csv,
        np.column_stack([xs, ys, zs, misfit_surface]),
        delimiter=",",
        header="x,y,z,time_integrated_misfit",
        comments="",
    )

    print("Saved CSV:", out_csv)

# ------------------------------------------------------------
# Plot surface maps
# ------------------------------------------------------------

def plot_surface_map(values, title, filename):
    plt.figure(figsize=(7, 6))
    sc = plt.scatter(xs, ys, c=values, s=8)
    plt.colorbar(sc, label="time-integrated misfit")
    plt.xlabel("x (m)")
    plt.ylabel("y (m)")
    plt.title(title)
    plt.axis("equal")
    plt.tight_layout()
    plt.savefig(FIG_DIR / filename, dpi=200)
    plt.close()

for field, values in results.items():
    plot_surface_map(
        values,
        f"Surface time-integrated misfit: {field}",
        f"surface_time_integrated_misfit_{field}.png",
    )

# ------------------------------------------------------------
# Also save one combined summary CSV
# ------------------------------------------------------------

summary_path = MISFIT_DIR / "surface_time_integrated_misfit_summary.csv"

combined = np.column_stack([
    xs,
    ys,
    zs,
    results["displ"],
    results["veloc"],
    results["accel"],
])

np.savetxt(
    summary_path,
    combined,
    delimiter=",",
    header="x,y,z,misfit_displ,misfit_veloc,misfit_accel",
    comments="",
)

print()
print("=" * 80)
print("Saved summary CSV:", summary_path)
print("Saved figures in:", FIG_DIR)
