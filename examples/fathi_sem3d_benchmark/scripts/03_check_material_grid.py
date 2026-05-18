import numpy as np
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data" / "processed"

target_path = DATA_DIR / "fathi_3d_material_grid_target.npz"
initial_path = DATA_DIR / "fathi_3d_material_grid_initial.npz"

target = np.load(target_path)
initial = np.load(initial_path)

print("Target file keys:")
print(target.files)
print()

print("Initial file keys:")
print(initial.files)
print()

x = target["x"]
y = target["y"]
z = target["z"]

lam_t = target["lambda_field"]
mu_t = target["mu_field"]
rho_t = target["rho_field"]
vp_t = target["vp_field"]
vs_t = target["vs_field"]

lam_i = initial["lambda_field"]
mu_i = initial["mu_field"]

print("Grid:")
print("x:", x.min(), x.max(), "number:", len(x))
print("y:", y.min(), y.max(), "number:", len(y))
print("z:", z.min(), z.max(), "number:", len(z))
print()

print("Target fields:")
print("lambda shape:", lam_t.shape)
print("mu shape:", mu_t.shape)
print("rho shape:", rho_t.shape)
print()

print("Target lambda MPa:", np.unique(lam_t) / 1e6)
print("Target mu MPa:", np.unique(mu_t) / 1e6)
print("Target rho:", np.unique(rho_t))
print()

print("Target Vp min/max:", vp_t.min(), vp_t.max())
print("Target Vs min/max:", vs_t.min(), vs_t.max())
print()

print("Initial lambda MPa:", np.unique(lam_i) / 1e6)
print("Initial mu MPa:", np.unique(mu_i) / 1e6)
