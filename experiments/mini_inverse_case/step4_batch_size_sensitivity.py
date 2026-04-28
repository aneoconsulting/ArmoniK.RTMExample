import numpy as np
import time
import os
import csv

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
    return [items[i:i + batch_size] for i in range(0, len(items), batch_size)]


def run_one_experiment(batch_size, parameters, t, u_obs):
    parameter_batches = split_into_batches(parameters, batch_size)

    start = time.time()

    with Pymonik(
        endpoint="172.25.249.249:5001",
        partition="pymonik",
        environment={"pip": ["numpy"]},
    ) as p:
        handles = []

        for batch in parameter_batches:
            handle = batch_forward_and_misfit.invoke(
                batch,
                t,
                u_obs,
                pymonik=p,
            )
            handles.append(handle)

        all_results = []

        for handle in handles:
            batch_result = handle.wait().get()
            all_results.extend(batch_result)

    end = time.time()

    results = np.array(all_results)
    best_idx = np.argmin(results[:, 2])
    best_A, best_f, best_J = results[best_idx]

    return {
        "batch_size": batch_size,
        "num_tasks": len(parameter_batches),
        "execution_time": end - start,
        "best_A": float(best_A),
        "best_f": float(best_f),
        "best_J": float(best_J),
    }


def main():
    t = np.linspace(0, 10, 1000)

    A_true = 2.0
    f_true = 1.5

    np.random.seed(42)
    u_obs = forward_simulation(t, A_true, f_true) + 0.05 * np.random.randn(len(t))

    A_values = np.linspace(1.0, 3.0, 41)
    f_values = np.linspace(0.8, 2.2, 41)

    parameters = []

    for A in A_values:
        for f in f_values:
            parameters.append((float(A), float(f)))

    batch_sizes = [1, 10, 50, 100, 200, 500]

    print("Batch size sensitivity experiment")
    print(f"Total parameter combinations = {len(parameters)}")
    print(f"True parameters: A={A_true}, f={f_true}")

    summary = []

    for batch_size in batch_sizes:
        print("\n--------------------------------")
        print(f"Running batch_size = {batch_size}")

        result = run_one_experiment(batch_size, parameters, t, u_obs)
        summary.append(result)

        print(f"Number of tasks = {result['num_tasks']}")
        print(f"Execution time = {result['execution_time']:.4f} s")
        print(f"Best A = {result['best_A']:.4f}")
        print(f"Best f = {result['best_f']:.4f}")
        print(f"Best misfit = {result['best_J']:.6f}")

    output_path = os.path.join(RESULTS_DIR, "batch_size_sensitivity.csv")

    with open(output_path, "w", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "batch_size",
                "num_tasks",
                "execution_time",
                "best_A",
                "best_f",
                "best_J",
            ],
        )
        writer.writeheader()
        writer.writerows(summary)

    print("\n================================")
    print("Summary")
    for r in summary:
        print(
            f"batch_size={r['batch_size']:>4} | "
            f"tasks={r['num_tasks']:>4} | "
            f"time={r['execution_time']:.4f}s | "
            f"best=({r['best_A']:.2f}, {r['best_f']:.2f})"
        )

    print(f"\nSaved summary to: {output_path}")


if __name__ == "__main__":
    main()