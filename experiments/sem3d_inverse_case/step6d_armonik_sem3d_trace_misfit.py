import os
import h5py
import numpy as np
from pymonik import task, Pymonik


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TRACE_DIR = os.path.join(BASE_DIR, "templates", "traces")
RESULTS_DIR = os.path.join(BASE_DIR, "results")
os.makedirs(RESULTS_DIR, exist_ok=True)


def list_h5_files():
    return sorted([
        os.path.join(TRACE_DIR, name)
        for name in os.listdir(TRACE_DIR)
        if name.endswith(".h5")
    ])


def list_stations(h5_path):
    with h5py.File(h5_path, "r") as h5:
        return sorted([
            k for k in h5.keys()
            if k.startswith("UU_") and not k.endswith("_pos")
        ])


def read_station_component(h5_path, station, component_index):
    with h5py.File(h5_path, "r") as h5:
        return h5[station][:, component_index]


def compute_misfit(u_sim, u_obs):
    n = min(len(u_sim), len(u_obs))
    return float(np.mean((u_sim[:n] - u_obs[:n]) ** 2))


@task
def compute_misfit_batch(batch_items, u_obs):
    results = []

    for item in batch_items:
        station = item["station"]
        h5_file = item["h5_file"]
        u_sim = np.array(item["trace"])

        J = compute_misfit(u_sim, u_obs)

        results.append({
            "h5_file": h5_file,
            "station": station,
            "misfit": J,
            "status": "OK",
        })

    return results


def main():
    component_index = 1  # Displ 1

    h5_files = list_h5_files()
    all_items = []

    for h5_path in h5_files:
        stations = list_stations(h5_path)

        for station in stations:
            trace = read_station_component(h5_path, station, component_index)

            all_items.append({
                "h5_file": os.path.basename(h5_path),
                "station": station,
                "trace": trace,
            })

    reference = all_items[0]
    u_obs = np.array(reference["trace"])

    batch_size = 20
    batches = [
        all_items[i:i + batch_size]
        for i in range(0, len(all_items), batch_size)
    ]

    print("ArmoniK SEM3D trace misfit experiment")
    print(f"Total stations = {len(all_items)}")
    print(f"Reference H5 file = {reference['h5_file']}")
    print(f"Reference station = {reference['station']}")
    print(f"Component index = {component_index}")
    print(f"Batch size = {batch_size}")
    print(f"Number of ArmoniK tasks = {len(batches)}")

    with Pymonik(
        endpoint="172.25.249.249:5001",
        partition="pymonik",
        environment={"pip": ["numpy"]},
    ) as p:
        tasks = []

        for batch in batches:
            t = compute_misfit_batch.invoke(
                batch,
                u_obs,
                pymonik=p,
            )
            tasks.append(t)

        all_results = []
        for t in tasks:
            all_results.extend(t.wait().get())

    all_results = sorted(all_results, key=lambda x: x["misfit"])

    output_csv = os.path.join(RESULTS_DIR, "sem3d_armonik_trace_misfits.csv")

    with open(output_csv, "w") as f:
        f.write("h5_file,station,misfit,status\n")
        for r in all_results:
            f.write(
                f"{r['h5_file']},"
                f"{r['station']},"
                f"{r['misfit']},"
                f"{r['status']}\n"
            )

    print("\nTop 10 closest traces:")
    for r in all_results[:10]:
        print(
            f"{r['h5_file']} | {r['station']} | "
            f"J={r['misfit']:.8e} | {r['status']}"
        )

    print(f"\nSaved results to: {output_csv}")


if __name__ == "__main__":
    main()