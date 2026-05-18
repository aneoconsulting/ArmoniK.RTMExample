import h5py
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parents[1]

runs = {
    "target": ROOT / "data" / "target_run",
    "initial": ROOT / "data" / "initial_run",
}

for name, run_dir in runs.items():
    print()
    print("=" * 80)
    print(name.upper(), run_dir)

    geom = run_dir / "res" / "geometry0000.h5"
    if not geom.exists():
        print("Missing geometry:", geom)
        continue

    with h5py.File(geom, "r") as f:
        nodes = f["Nodes"][:]
        lamb = f["Lamb"][:]
        mu = f["Mu"][:]
        dens = f["Dens"][:]

        print("Nodes:", nodes.shape)
        print("x range:", nodes[:, 0].min(), nodes[:, 0].max())
        print("y range:", nodes[:, 1].min(), nodes[:, 1].max())
        print("z range:", nodes[:, 2].min(), nodes[:, 2].max())
        print("Lamb min/max:", lamb.min(), lamb.max())
        print("Mu   min/max:", mu.min(), mu.max())
        print("Dens min/max:", dens.min(), dens.max())
        print("Unique Lamb approx:", np.unique(np.round(lamb, -2))[:10], "...")
        print("Unique Mu approx:", np.unique(np.round(mu, -2))[:10], "...")

    rsems = sorted((run_dir / "res").glob("Rsem*"))
    print("Number of snapshots:", len(rsems))
    if rsems:
        print("First snapshot:", rsems[0].name)
        print("Last snapshot:", rsems[-1].name)

        sample = rsems[min(9, len(rsems)-1)] / "sem_field.0000.h5"
        print("Sample field:", sample.relative_to(ROOT))
        with h5py.File(sample, "r") as f:
            for key in f.keys():
                arr = f[key]
                print(" ", key, arr.shape, arr.dtype)
