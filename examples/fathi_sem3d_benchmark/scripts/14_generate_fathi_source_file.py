import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
FIG_DIR = ROOT / "results" / "figures"
FIG_DIR.mkdir(parents=True, exist_ok=True)

# Fathi p20 Gaussian pulse parameters
mu_bar = 0.11
sigma_bar = 0.0014
t_end = 0.20

# Use a fine time sampling for the source file
dt = 1e-4
t = np.arange(0.0, t_end + dt, dt)

# Gaussian pulse
f = np.exp(-((t - mu_bar) / sigma_bar) ** 2)

# Optional amplitude scaling.
# Fathi mentions a vertical stress load with amplitude 1 kPa.
# For now, keep normalized amplitude = 1.0.
# If SEM3D expects physical force amplitude here, use amp = 1000.0.
amp = 1.0
source = amp * f

for run in ["target_run", "initial_run"]:
    out_path = ROOT / "data" / run / "source_p20.txt"
    np.savetxt(
        out_path,
        np.column_stack([t, source]),
        fmt="%.8e",
        header="time amplitude",
        comments="",
    )
    print("Saved:", out_path)

plt.figure(figsize=(7, 4))
plt.plot(t, source)
plt.xlabel("time (s)")
plt.ylabel("amplitude")
plt.title("Fathi p20 Gaussian source file")
plt.grid(True)
plt.tight_layout()
plt.savefig(FIG_DIR / "fathi_p20_source_file.png", dpi=200)
plt.close()

print("Saved figure:", FIG_DIR / "fathi_p20_source_file.png")
print("max amplitude:", source.max())
print("time at max:", t[np.argmax(source)])
