import os
import h5py
import numpy as np
import matplotlib.pyplot as plt


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_DIR = os.path.join(BASE_DIR, "templates")
TRACE_DIR = os.path.join(TEMPLATE_DIR, "traces")
RESULTS_DIR = os.path.join(BASE_DIR, "results")

os.makedirs(RESULTS_DIR, exist_ok=True)


def list_stations(h5_path):
    with h5py.File(h5_path, "r") as h5:
        return sorted([
            k for k in h5.keys()
            if k.startswith("UU_") and not k.endswith("_pos")
        ])


def read_variables(h5_path):
    with h5py.File(h5_path, "r") as h5:
        return [v.decode("utf-8").strip() for v in h5["Variables"][:]]


def read_station_component(h5_path, station, component_index):
    with h5py.File(h5_path, "r") as h5:
        return h5[station][:, component_index]


def compute_misfit(u1, u2):
    n = min(len(u1), len(u2))
    return float(np.mean((u1[:n] - u2[:n]) ** 2))


def main():
    h5_files = sorted([
        os.path.join(TRACE_DIR, name)
        for name in os.listdir(TRACE_DIR)
        if name.endswith(".h5")
    ])

    print("H5 files:")
    for f in h5_files:
        print(f)

    station_file_map = {}

    print("\nStations per file:")
    for f in h5_files:
        stations = list_stations(f)
        print(os.path.basename(f), ":", stations[:10], f"(total={len(stations)})")
        for s in stations:
            station_file_map[s] = f

    all_stations = sorted(station_file_map.keys())

    if not all_stations:
        raise RuntimeError("No station found.")

    station = all_stations[0]
    h5_path = station_file_map[station]

    variables = read_variables(h5_path)

    print("\nVariables:")
    for i, name in enumerate(variables):
        print(f"{i}: {name}")

    component_obs = 1  # Displ 1
    component_sim = 2  # Displ 2, just for pipeline test

    print("\nSelected station:")
    print(station)
    print("Located in:")
    print(h5_path)

    print(f"\nReference component = {component_obs}: {variables[component_obs]}")
    print(f"Compared component  = {component_sim}: {variables[component_sim]}")

    u_obs = read_station_component(h5_path, station, component_obs)
    u_sim = read_station_component(h5_path, station, component_sim)

    J = compute_misfit(u_sim, u_obs)

    print("\nPipeline test misfit:")
    print(f"misfit = {J:.8e}")

    output_csv = os.path.join(RESULTS_DIR, "sem3d_trace_misfit_test.csv")
    np.savetxt(
        output_csv,
        np.array([[J]]),
        delimiter=",",
        header="misfit",
        comments=""
    )

    output_png = os.path.join(RESULTS_DIR, "sem3d_trace_component_comparison.png")

    plt.figure(figsize=(10, 5))
    plt.plot(u_obs, label=variables[component_obs], linewidth=1)
    plt.plot(u_sim, label=variables[component_sim], linewidth=1)
    plt.xlabel("Time step")
    plt.ylabel("Amplitude")
    plt.title(f"SEM3D trace component comparison: {station}")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(output_png, dpi=200)
    plt.close()

    print(f"\nSaved CSV to: {output_csv}")
    print(f"Saved plot to: {output_png}")


if __name__ == "__main__":
    main()