# Mini inverse case with ArmoniK

This example implements a small inverse problem to test ArmoniK on a parameter scan workflow.

The toy forward model is a damped sinusoidal trace:

```text
u(t; A, f) = A sin(2π f t) exp(-0.3 t)
The objective is to recover the true parameters (A, f) by minimizing the misfit between a synthetic observed trace and simulated traces.
Steps
step1_sequential.py
Sequential Python baseline.
step2_armonik_tasks.py
One ArmoniK task per parameter combination.
step3_armonik_batch_tasks.py
Batched ArmoniK tasks.
step4_batch_size_sensitivity.py
Sensitivity experiment on the batch size.
step5_batch_performance_plots.py
Performance visualization.
Main result

The experiment shows that task granularity is critical in ArmoniK workflows.

Very small tasks lead to high scheduling overhead. Batching several parameter combinations into one task significantly reduces execution time while preserving the same optimal parameters.
Batch-size sensitivity result
batch_size	number_of_tasks	execution_time
1	1681	268.9542 s
10	169	25.5903 s
50	34	5.3970 s
100	17	2.3710 s
200	9	1.2815 s
500	4	0.6148 s
Generated outputs

The scripts generate result files under:
experiments/mini_inverse_case/results/
Main files:

batch_size_sensitivity.csv
batch_size_vs_time.png
num_tasks_vs_time.png
performance_summary.png
Local ArmoniK configuration

Before running ArmoniK scripts locally:

export AKCONFIG=/home/ywang/ArmoniK/infrastructure/quick-deploy/localhost/generate
The local scripts currently use:

endpoint="172.25.249.249:5001"
partition="pymonik"

These values may need to be changed depending on the local ArmoniK deployment.
