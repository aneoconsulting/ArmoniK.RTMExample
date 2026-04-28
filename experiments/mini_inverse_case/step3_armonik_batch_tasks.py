import numpy as np
import time
import os

from pymonik import task, Pymonik


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RESULTS_DIR = os.path.join(BASE_DIR, "results")
os.makedirs(RESULTS_DIR, exist_ok=True)


@task
def batch_forward_and_misfit(parameter_batch, t, u_obs):
    batch_results = []

    for A, f in parameter_batch:
        u_sim = A * np.sin(2 * np.pi * f * t) * np.exp(-0.3 * t)
        misfit = np.mean((u_sim - u_obs) ** 2)
        batch_results.append((A, f, misfit))

    return batch_results


def forward_simulation(t, A, f):
    return A * np.sin(2 * np.pi * f * t) * np.exp(-0.3 * t)


def split_into_batches(items, batch_size):
    batches = []

    for i in range(0, len(items), batch_size):
        batches.append(items[i:i + batch_size])

    return batches


def main():
    t = np.linspace(0, 10, 1000)

    A_true = 2.0
    f_true = 1.5

    np.random.seed(42)
    clean_obs = forward_simulation(t, A_true, f_true)
    noise = 0.05 * np.random.randn(len(t))
    u_obs = clean_obs + noise

    A_values = np.linspace(1.0, 3.0, 41)
    f_values = np.linspace(0.8, 2.2, 41)

    parameters = []

    for A in A_values:
        for f in f_values:
            parameters.append((float(A), float(f)))

    batch_size = 100
    parameter_batches = split_into_batches(parameters, batch_size)

    print("Batch task version")
    print(f"Total parameter combinations = {len(parameters)}")
    print(f"Batch size = {batch_size}")
    print(f"Number of ArmoniK tasks = {len(parameter_batches)}")

    start = time.time()

    with Pymonik(
        endpoint="172.25.249.249:5001",
        partition="pymonik",
        environment={"pip": ["numpy"]},
    ) as p:
        task_handles = []

        for batch in parameter_batches:
            handle = batch_forward_and_misfit.invoke(
                batch,
                t,
                u_obs,
                pymonik=p,
            )
            task_handles.append(handle)

        all_results = []

        for handle in task_handles:
            batch_result = handle.wait().get()
            all_results.extend(batch_result)

    end = time.time()

    results = np.array(all_results)

    best_idx = np.argmin(results[:, 2])
    best_A, best_f, best_J = results[best_idx]

    print("\nTrue parameters:")
    print(f"A_true = {A_true}, f_true = {f_true}")

    print("\nBest estimated parameters with ArmoniK batch tasks:")
    print(f"A_best = {best_A:.4f}")
    print(f"f_best = {best_f:.4f}")
    print(f"misfit = {best_J:.6f}")

    print("\nExecution time with ArmoniK batch tasks:")
    print(f"{end - start:.4f} seconds")

    output_path = os.path.join(RESULTS_DIR, "armonik_batch_parameter_scan_results.csv")
    np.savetxt(
        output_path,
        results,
        delimiter=",",
        header="A,f,misfit",
        comments=""
    )

    print(f"\nSaved results to: {output_path}")


if __name__ == "__main__":
    main()