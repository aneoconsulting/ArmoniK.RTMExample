import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data" / "processed"
FIG_DIR = ROOT / "results" / "figures"

DATA_DIR.mkdir(parents=True, exist_ok=True)
FIG_DIR.mkdir(parents=True, exist_ok=True)

# ------------------------------------------------------------
# Fathi et al. 2015 layered benchmark
# Domain: 40 m x 40 m x 45 m
# We use a simple regular material grid here.
# This is NOT yet the SEM3D GLL grid.
# ------------------------------------------------------------

dx = 1.0
dy = 1.0
dz = 1.0

x = np.arange(-20.0, 20.0 + dx, dx)
y = np.arange(-20.0, 20.0 + dy, dy)
z = np.arange(0.0, -45.0 - dz, -dz)

X, Y, Z = np.meshgrid(x, y, z, indexing="ij")

rho = np.full_like(X, 2000.0, dtype=float)

lam_target = np.zeros_like(X, dtype=float)
mu_target = np.zeros_like(X, dtype=float)

# Layer 1: -12 <= z <= 0
mask1 = (Z >= -12.0) & (Z <= 0.0)

# Layer 2: -27 <= z < -12
mask2 = (Z >= -27.0) & (Z < -12.0)

# Layer 3: z < -27
mask3 = Z < -27.0

lam_target[mask1] = 80e6
mu_target[mask1] = 80e6

lam_target[mask2] = 101.25e6
mu_target[mask2] = 101.25e6

lam_target[mask3] = 125e6
mu_target[mask3] = 125e6

# Initial model: homogeneous model
lam_initial = np.full_like(X, 80e6, dtype=float)
mu_initial = np.full_like(X, 80e6, dtype=float)
rho_initial = np.full_like(X, 2000.0, dtype=float)

vp_target = np.sqrt((lam_target + 2.0 * mu_target) / rho)
vs_target = np.sqrt(mu_target / rho)

vp_initial = np.sqrt((lam_initial + 2.0 * mu_initial) / rho_initial)
vs_initial = np.sqrt(mu_initial / rho_initial)

np.savez(
    DATA_DIR / "fathi_3d_material_grid_target.npz",
    x=x,
    y=y,
    z=z,
    X=X,
    Y=Y,
    Z=Z,
    lambda_field=lam_target,
    mu_field=mu_target,
    rho_field=rho,
    vp_field=vp_target,
    vs_field=vs_target,
)

np.savez(
    DATA_DIR / "fathi_3d_material_grid_initial.npz",
    x=x,
    y=y,
    z=z,
    X=X,
    Y=Y,
    Z=Z,
    lambda_field=lam_initial,
    mu_field=mu_initial,
    rho_field=rho_initial,
    vp_field=vp_initial,
    vs_field=vs_initial,
)

# Save a CSV version for inspection
flat_target = np.column_stack([
    X.ravel(),
    Y.ravel(),
    Z.ravel(),
    lam_target.ravel(),
    mu_target.ravel(),
    rho.ravel(),
    vp_target.ravel(),
    vs_target.ravel(),
])

np.savetxt(
    DATA_DIR / "fathi_3d_material_grid_target.csv",
    flat_target,
    delimiter=",",
    header="x,y,z,lambda,mu,rho,vp,vs",
    comments="",
)

# ------------------------------------------------------------
# Plot vertical section at y = 0
# ------------------------------------------------------------

iy0 = np.argmin(np.abs(y - 0.0))

plt.figure(figsize=(7, 5))
plt.imshow(
    lam_target[:, iy0, :].T / 1e6,
    origin="upper",
    extent=[x.min(), x.max(), z.min(), z.max()],
    aspect="auto",
)
plt.colorbar(label="lambda (MPa)")
plt.xlabel("x (m)")
plt.ylabel("z (m)")
plt.title("Target lambda field, vertical section y=0")
plt.tight_layout()
plt.savefig(FIG_DIR / "target_lambda_vertical_section_y0.png", dpi=200)

plt.figure(figsize=(7, 5))
plt.imshow(
    mu_target[:, iy0, :].T / 1e6,
    origin="upper",
    extent=[x.min(), x.max(), z.min(), z.max()],
    aspect="auto",
)
plt.colorbar(label="mu (MPa)")
plt.xlabel("x (m)")
plt.ylabel("z (m)")
plt.title("Target mu field, vertical section y=0")
plt.tight_layout()
plt.savefig(FIG_DIR / "target_mu_vertical_section_y0.png", dpi=200)

# ------------------------------------------------------------
# Plot horizontal sections
# ------------------------------------------------------------

for depth in [-6.0, -18.0, -35.0]:
    iz = np.argmin(np.abs(z - depth))

    plt.figure(figsize=(6, 5))
    plt.imshow(
        lam_target[:, :, iz].T / 1e6,
        origin="lower",
        extent=[x.min(), x.max(), y.min(), y.max()],
        aspect="equal",
    )
    plt.colorbar(label="lambda (MPa)")
    plt.xlabel("x (m)")
    plt.ylabel("y (m)")
    plt.title(f"Target lambda horizontal section z={z[iz]:.1f} m")
    plt.tight_layout()
    plt.savefig(FIG_DIR / f"target_lambda_horizontal_z_{abs(int(z[iz]))}m.png", dpi=200)

print("3D material grids generated successfully.")
print()
print("Target NPZ:")
print(DATA_DIR / "fathi_3d_material_grid_target.npz")
print()
print("Initial NPZ:")
print(DATA_DIR / "fathi_3d_material_grid_initial.npz")
print()
print("Target CSV:")
print(DATA_DIR / "fathi_3d_material_grid_target.csv")
print()
print("Figures saved in:")
print(FIG_DIR)
print()
print("Grid shape:", X.shape)
print("Number of material grid points:", X.size)
print()
print("Target lambda unique values in MPa:")
print(np.unique(lam_target) / 1e6)
print()
print("Target mu unique values in MPa:")
print(np.unique(mu_target) / 1e6)
print()
print("Initial lambda unique values in MPa:")
print(np.unique(lam_initial) / 1e6)
