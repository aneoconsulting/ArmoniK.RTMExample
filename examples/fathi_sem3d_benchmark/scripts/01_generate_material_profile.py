import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIG_DIR = ROOT / "results" / "figures"
FIG_DIR.mkdir(parents=True, exist_ok=True)

rho = 2000.0

z = np.linspace(0.0, -45.0, 451)

lam = np.zeros_like(z)
mu = np.zeros_like(z)

for i, zi in enumerate(z):
    if -12.0 <= zi <= 0.0:
        lam[i] = 80e6
        mu[i] = 80e6
    elif -27.0 <= zi < -12.0:
        lam[i] = 101.25e6
        mu[i] = 101.25e6
    else:
        lam[i] = 125e6
        mu[i] = 125e6

vp = np.sqrt((lam + 2.0 * mu) / rho)
vs = np.sqrt(mu / rho)

np.savetxt(
    ROOT / "data" / "processed" / "fathi_layered_profile.csv",
    np.column_stack([z, lam, mu, vp, vs]),
    delimiter=",",
    header="z,lambda,mu,vp,vs",
    comments=""
)

plt.figure(figsize=(6, 6))
plt.plot(lam / 1e6, z, label="lambda")
plt.plot(mu / 1e6, z, "--", label="mu")
plt.xlabel("Lamé parameters (MPa)")
plt.ylabel("Depth z (m)")
plt.title("Fathi et al. 2015 layered target model")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.savefig(FIG_DIR / "fathi_layered_lambda_mu_profile.png", dpi=200)

plt.figure(figsize=(6, 6))
plt.plot(vp, z, label="Vp")
plt.plot(vs, z, label="Vs")
plt.xlabel("Velocity (m/s)")
plt.ylabel("Depth z (m)")
plt.title("Velocity profile from lambda and mu")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.savefig(FIG_DIR / "fathi_layered_velocity_profile.png", dpi=200)

print("Generated material profile:")
print("CSV:", ROOT / "data" / "processed" / "fathi_layered_profile.csv")
print("Figure 1:", FIG_DIR / "fathi_layered_lambda_mu_profile.png")
print("Figure 2:", FIG_DIR / "fathi_layered_velocity_profile.png")
print()
print("lambda min/max:", lam.min(), lam.max())
print("mu min/max:", mu.min(), mu.max())
print("Vp min/max:", vp.min(), vp.max())
print("Vs min/max:", vs.min(), vs.max())
