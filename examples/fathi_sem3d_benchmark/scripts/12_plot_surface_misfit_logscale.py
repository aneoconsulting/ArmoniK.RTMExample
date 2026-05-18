import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CSV = ROOT / "results" / "misfit" / "surface_time_integrated_misfit_summary.csv"
FIG_DIR = ROOT / "results" / "figures"
FIG_DIR.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(CSV)

x = df["x"].to_numpy()
y = df["y"].to_numpy()

for col in ["misfit_displ", "misfit_veloc", "misfit_accel"]:
    values = df[col].to_numpy()

    log_values = np.log10(values + 1e-30)

    plt.figure(figsize=(7, 6))
    sc = plt.scatter(x, y, c=log_values, s=8)
    plt.colorbar(sc, label=f"log10({col})")
    plt.xlabel("x (m)")
    plt.ylabel("y (m)")
    plt.title(f"Surface time-integrated misfit map: {col}")
    plt.axis("equal")
    plt.tight_layout()
    plt.savefig(FIG_DIR / f"surface_time_integrated_{col}_log10.png", dpi=200)
    plt.close()

    print(col, "min/max:", values.min(), values.max())

print("Saved log-scale maps in:", FIG_DIR)
