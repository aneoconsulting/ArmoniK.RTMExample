import numpy as np
import matplotlib.pyplot as plt
import time
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RESULTS_DIR = os.path.join(BASE_DIR, "results")
os.makedirs(RESULTS_DIR, exist_ok=True)

def forward_simulation(t, A, f):
    return A * np.sin(2 * np.pi * f * t) * np.exp(-0.3 * t)

def compute_misfit(u_sim, u_obs):
    return np.mean((u_sim - u_obs) ** 2)

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

    results = []

    start = time.time()

    for A in A_values:
        for f in f_values:
            u_sim = forward_simulation(t, A, f)
            J = compute_misfit(u_sim, u_obs)
            results.append((A, f, J))

    end = time.time()

    results = np.array(results)
    best_idx = np.argmin(results[:, 2])
    best_A, best_f, best_J = results[best_idx]

    print("True parameters:")
    print(f"A_true = {A_true}, f_true = {f_true}")

    print("\nBest estimated parameters:")
    print(f"A_best = {best_A:.4f}, f_best = {best_f:.4f}, misfit = {best_J:.6f}")

    print("\nExecution time:")
    print(f"{end - start:.4f} seconds")

    u_best = forward_simulation(t, best_A, best_f)

    plt.figure(figsize=(10, 5))
    plt.plot(t, u_obs, label="Observed trace", linewidth=1)
    plt.plot(t, u_best, label="Best simulated trace", linewidth=1)
    plt.xlabel("Time")
    plt.ylabel("Amplitude")
    plt.title("Observed trace vs best simulated trace")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(os.path.join(RESULTS_DIR, "trace_comparison.png"), dpi=200)

    misfit_grid = results[:, 2].reshape(len(A_values), len(f_values))

    plt.figure(figsize=(8, 6))
    plt.imshow(
        misfit_grid,
        extent=[f_values.min(), f_values.max(), A_values.min(), A_values.max()],
        origin="lower",
        aspect="auto"
    )
    plt.colorbar(label="Misfit")
    plt.scatter([f_true], [A_true], marker="x", label="True parameter")
    plt.scatter([best_f], [best_A], marker="o", label="Best estimated")
    plt.xlabel("Frequency f")
    plt.ylabel("Amplitude A")
    plt.title("Misfit landscape")
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(RESULTS_DIR, "misfit_heatmap.png"), dpi=200)

    np.savetxt(
        os.path.join(RESULTS_DIR, "parameter_scan_results.csv"),
        results,
        delimiter=",",
        header="A,f,misfit",
        comments=""
    )

if __name__ == "__main__":
    main()