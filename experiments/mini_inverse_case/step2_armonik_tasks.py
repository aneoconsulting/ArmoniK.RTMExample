import numpy as np
import time
import os

from pymonik import task, Pymonik


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RESULTS_DIR = os.path.join(BASE_DIR, "results")
os.makedirs(RESULTS_DIR, exist_ok=True)


@task
def forward_and_misfit(A, f, t, u_obs):
    u_sim = A * np.sin(2 * np.pi * f * t) * np.exp(-0.3 * t)
    misfit = np.mean((u_sim - u_obs) ** 2)
    return A, f, misfit


@task
def aggregate_results(results):
    results = np.array(results)

    best_idx = np.argmin(results[:, 2])
    best_A, best_f, best_J = results[best_idx]

    return {
        "best_A": float(best_A),
        "best_f": float(best_f),
        "best_J": float(best_J),
        "all_results": results.tolist(),
    }


def forward_simulation(t, A, f):
    return A * np.sin(2 * np.pi * f * t) * np.exp(-0.3 * t)


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

    start = time.time()

    with Pymonik(
        endpoint="172.25.249.249:5001",
        partition="pymonik",
        environment={"pip": ["numpy"]},
    ) as p:
        tasks = []

        for A in A_values:
            for f in f_values:
                task_result = forward_and_misfit.invoke(
                    float(A),
                    float(f),
                    t,
                    u_obs,
                    pymonik=p,
                )
                tasks.append(task_result)

        results = []

        for task_result in tasks:
            results.append(task_result.wait().get())

        results = np.array(results)

        best_idx = np.argmin(results[:, 2])
        best_A, best_f, best_J = results[best_idx]

        final_result = {
            "best_A": float(best_A),
            "best_f": float(best_f),
            "best_J": float(best_J),
            "all_results": results.tolist(),
        }

    end = time.time()

    print("True parameters:")
    print(f"A_true = {A_true}, f_true = {f_true}")

    print("\nBest estimated parameters with ArmoniK:")
    print(f"A_best = {final_result['best_A']:.4f}")
    print(f"f_best = {final_result['best_f']:.4f}")
    print(f"misfit = {final_result['best_J']:.6f}")

    print("\nExecution time with ArmoniK:")
    print(f"{end - start:.4f} seconds")

    output_path = os.path.join(RESULTS_DIR, "armonik_parameter_scan_results.csv")
    np.savetxt(
        output_path,
        np.array(final_result["all_results"]),
        delimiter=",",
        header="A,f,misfit",
        comments=""
    )

    print(f"\nSaved results to: {output_path}")


if __name__ == "__main__":
    main()