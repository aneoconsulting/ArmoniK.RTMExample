import os
import pandas as pd
import matplotlib.pyplot as plt


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RESULTS_DIR = os.path.join(BASE_DIR, "results")

csv_path = os.path.join(RESULTS_DIR, "batch_size_sensitivity.csv")

print("Generating performance plots...")
print(f"Reading summary from: {csv_path}")

df = pd.read_csv(csv_path)

batch_sizes = df["batch_size"]
num_tasks = df["num_tasks"]
execution_times = df["execution_time"]

plt.figure(figsize=(8, 5))
plt.plot(batch_sizes, execution_times, marker="o", label="ArmoniK batch tasks")
plt.xscale("log")
plt.yscale("log")
plt.xlabel("Batch size")
plt.ylabel("Execution time (s)")
plt.title("Batch size vs Execution time")
plt.grid(True, which="both", linestyle="--", alpha=0.5)
plt.legend()

for x, y in zip(batch_sizes, execution_times):
    plt.text(x, y, f"{y:.4f}", fontsize=9)

output1 = os.path.join(RESULTS_DIR, "batch_size_vs_time.png")
plt.tight_layout()
plt.savefig(output1, dpi=200)
plt.close()

plt.figure(figsize=(8, 5))
plt.plot(num_tasks, execution_times, marker="o", label="ArmoniK batch tasks")
plt.xscale("log")
plt.yscale("log")
plt.xlabel("Number of ArmoniK tasks")
plt.ylabel("Execution time (s)")
plt.title("Number of tasks vs Execution time")
plt.grid(True, which="both", linestyle="--", alpha=0.5)
plt.legend()

for x, y in zip(num_tasks, execution_times):
    plt.text(x, y, f"{y:.4f}", fontsize=9)

output2 = os.path.join(RESULTS_DIR, "num_tasks_vs_time.png")
plt.tight_layout()
plt.savefig(output2, dpi=200)
plt.close()

plt.figure(figsize=(12, 8))

plt.subplot(2, 1, 1)
plt.plot(batch_sizes, execution_times, marker="o")
plt.xscale("log")
plt.yscale("log")
plt.xlabel("Batch size")
plt.ylabel("Execution time (s)")
plt.title("Batch size vs Execution time")
plt.grid(True, which="both", linestyle="--", alpha=0.5)

plt.subplot(2, 1, 2)
plt.plot(num_tasks, execution_times, marker="o")
plt.xscale("log")
plt.yscale("log")
plt.xlabel("Number of ArmoniK tasks")
plt.ylabel("Execution time (s)")
plt.title("Number of tasks vs Execution time")
plt.grid(True, which="both", linestyle="--", alpha=0.5)

output3 = os.path.join(RESULTS_DIR, "performance_summary.png")
plt.tight_layout()
plt.savefig(output3, dpi=200)
plt.close()

print(f"Saved plot: {output1}")
print(f"Saved plot: {output2}")
print(f"Saved plot: {output3}")
print("Plots generated successfully.")