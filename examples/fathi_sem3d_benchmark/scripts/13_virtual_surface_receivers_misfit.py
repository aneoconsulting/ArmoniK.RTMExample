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

FIELDS = ["displ", "veloc", "accel"]
dt_snapshot = 0.02

# ------------------------------------------------------------
# Read geometry
# ------------------------------------------------------------

with h5py.File(TARGET / "geometry0000.h5", "r") as f:
    nodes = f["Nodes"][:]

x = nodes[:, 0]
y = nodes[:, 1]
z = nodes[:, 2]

z_surface = z.max()
surface_mask = np.abs(z - z_surface) < 1e-5
surface_indices = np.where(surface_mask)[0]

xs_all = x[surface_indices]
ys_all = y[surface_indices]

print("Surface z:", z_surface)
print("Number of surface GLL nodes:", len(surface_indices))

# ------------------------------------------------------------
# Define virtual receiver layout
# ------------------------------------------------------------
# Realistic surface receiver grid, not every GLL node.

receiver_coords = []

receiver_axis = np.array([-15.0, -10.0, -5.0, 0.0, 5.0, 10.0, 15.0])

for rx in receiver_axis:
    for ry in receiver_axis:
        receiver_coords.append([rx, ry, z_surface])

receiver_coords = np.array(receiver_coords, dtype=float)

# Find nearest surface GLL node for each receiver
receiver_node_indices = []
receiver_actual_coords = []

for rx, ry, rz in receiver_coords:
    dist2 = (xs_all - rx) ** 2 + (ys_all - ry) ** 2
    local_id = int(np.argmin(dist2))
    global_id = int(surface_indices[local_id])

    receiver_node_indices.append(global_id)
    receiver_actual_coords.append(nodes[global_id])

receiver_node_indices = np.array(receiver_node_indices, dtype=int)
receiver_actual_coords = np.array(receiver_actual_coords, dtype=float)

print("Number of virtual receivers:", len(receiver_node_indices))
print("First receivers:")
for i in range(min(10, len(receiver_node_indices))):
    print(
        i,
        "requested=", receiver_coords[i],
        "actual=", receiver_actual_coords[i],
        "node_id=", receiver_node_indices[i],
    )

# ------------------------------------------------------------
# Find common snapshots
# ------------------------------------------------------------

target_frames = sorted([p.name for p in TARGET.glob("Rsem*")])
initial_frames = sorted([p.name for p in INITIAL.glob("Rsem*")])
frames = sorted(set(target_frames).intersection(initial_frames))

print("Common frames:", len(frames), frames[0], frames[-1])

# ------------------------------------------------------------
# Compute time-integrated misfit at virtual receivers
# ------------------------------------------------------------

results = {}

for field in FIELDS:
    print()
    print("=" * 80)
    print("Computing receiver misfit for:", field)

    misfit = np.zeros(len(receiver_node_indices), dtype=np.float64)

    for frame in frames:
        target_path = TARGET / frame / "sem_field.0000.h5"
        initial_path = INITIAL / frame / "sem_field.0000.h5"

        # h5py requires fancy indices to be in increasing order.
        # We sort node indices for reading, then restore the original receiver order.
        sort_order = np.argsort(receiver_node_indices)
        sorted_indices = receiver_node_indices[sort_order]
        restore_order = np.argsort(sort_order)

        with h5py.File(target_path, "r") as ft:
            u_t_sorted = ft[field][sorted_indices, :].astype(np.float64)

        with h5py.File(initial_path, "r") as fi:
            u_i_sorted = fi[field][sorted_indices, :].astype(np.float64)

        u_t = u_t_sorted[restore_order, :]
        u_i = u_i_sorted[restore_order, :]

        diff = u_i - u_t
        misfit += np.sum(diff ** 2, axis=1) * dt_snapshot

    results[field] = misfit
    total_misfit = 0.5 * misfit.sum()
    
    print("total J =", total_misfit)
    print("min/max:", misfit.min(), misfit.max())
    print("mean:", misfit.mean())
    print("sum:", misfit.sum())

# ------------------------------------------------------------
# Save summary CSV
# ------------------------------------------------------------
total_rows = []

for field in FIELDS:
    local_sum = results[field].sum()
    total_J = 0.5 * local_sum
    total_rows.append([field, local_sum, total_J, len(receiver_node_indices)])

total_path = MISFIT_DIR / "total_receiver_misfit.csv"

with open(total_path, "w") as f:
    f.write("field,sum_local_misfit,total_J,number_of_receivers\n")
    for row in total_rows:
        f.write(",".join(map(str, row)) + "\n")

print()
print("=" * 80)
print("Total receiver misfit:")
for field, local_sum, total_J, nrec in total_rows:
    print(f"{field}: sum_local_misfit={local_sum:.6e}, total_J=0.5*sum={total_J:.6e}, nrec={nrec}")

print("Saved total misfit CSV:", total_path)
summary = np.column_stack([
    receiver_coords[:, 0],
    receiver_coords[:, 1],
    receiver_coords[:, 2],
    receiver_actual_coords[:, 0],
    receiver_actual_coords[:, 1],
    receiver_actual_coords[:, 2],
    receiver_node_indices,
    results["displ"],
    results["veloc"],
    results["accel"],
])

summary_path = MISFIT_DIR / "virtual_surface_receivers_time_integrated_misfit.csv"

np.savetxt(
    summary_path,
    summary,
    delimiter=",",
    header=(
        "requested_x,requested_y,requested_z,"
        "actual_x,actual_y,actual_z,node_id,"
        "misfit_displ,misfit_veloc,misfit_accel"
    ),
    comments="",
)

print()
print("Saved CSV:", summary_path)

# ------------------------------------------------------------
# Plot receiver misfit maps
# ------------------------------------------------------------

rx = receiver_coords[:, 0]
ry = receiver_coords[:, 1]

def plot_map(values, title, filename, logscale=False):
    if logscale:
        plot_values = np.log10(values + 1e-30)
        label = "log10(time-integrated misfit)"
    else:
        plot_values = values
        label = "time-integrated misfit"

    plt.figure(figsize=(7, 6))
    sc = plt.scatter(rx, ry, c=plot_values, s=120, marker="s")
    plt.colorbar(sc, label=label)
    plt.xlabel("receiver x (m)")
    plt.ylabel("receiver y (m)")
    plt.title(title)
    plt.axis("equal")
    plt.tight_layout()
    plt.savefig(FIG_DIR / filename, dpi=200)
    plt.close()

for field in FIELDS:
    plot_map(
        results[field],
        f"Virtual receivers time-integrated misfit: {field}",
        f"virtual_receivers_misfit_{field}.png",
        logscale=False,
    )

    plot_map(
        results[field],
        f"Virtual receivers log misfit: {field}",
        f"virtual_receivers_misfit_{field}_log10.png",
        logscale=True,
    )

print("Saved figures in:", FIG_DIR)
#_________

total_rows = []

for field in FIELDS:
    sum_local = results[field].sum()
    total_J = 0.5 * sum_local
    total_rows.append([field, sum_local, total_J, len(receiver_node_indices)])

total_path = MISFIT_DIR / "total_receiver_misfit.csv"

with open(total_path, "w") as f:
    f.write("field,sum_local_misfit,total_J,number_of_receivers\n")
    for row in total_rows:
        f.write(",".join(map(str, row)) + "\n")

print()
print("=" * 80)
print("Total receiver misfit:")
for field, sum_local, total_J, nrec in total_rows:
    print(f"{field}: sum_local={sum_local:.6e}, total_J={total_J:.6e}, nrec={nrec}")

print("Saved:", total_path)
