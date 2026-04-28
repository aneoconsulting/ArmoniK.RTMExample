# Mini Inverse Case with ArmoniK

A small inverse problem benchmark to test ArmoniK on a **parameter scan workflow**.

## Problem Statement

The toy forward model is a damped sinusoidal trace:

```text
u(t; A, f) = A·sin(2π f t)·exp(-0.3 t)
```

The goal is to recover the true parameters **(A, f)** by minimizing the misfit between a synthetic observed trace and simulated traces.

---

## Workflow Steps

| Script | Description |
|---|---|
| `step1_sequential.py` | Sequential Python baseline |
| `step2_armonik_tasks.py` | One ArmoniK task per parameter combination |
| `step3_armonik_batch_tasks.py` | Batched ArmoniK tasks |
| `step4_batch_size_sensitivity.py` | Sensitivity experiment on batch size |
| `step5_batch_performance_plots.py` | Performance visualization |

---

## Main Result

Task granularity is critical in ArmoniK workflows:

- **Very small tasks** → high scheduling overhead
- **Batched tasks** → significantly reduced execution time, same optimal parameters

### Batch-Size Sensitivity

| `batch_size` | `number_of_tasks` | `execution_time` |
|:---:|:---:|:---:|
| 1 | 1681 | 268.95 s |
| 10 | 169 | 25.59 s |
| 50 | 34 | 5.40 s |
| 100 | 17 | 2.37 s |
| 200 | 9 | 1.28 s |
| 500 | 4 | 0.61 s |

---

## Generated Outputs

Results are written to `experiments/mini_inverse_case/results/`:

```
results/
├── batch_size_sensitivity.csv
├── batch_size_vs_time.png
├── num_tasks_vs_time.png
└── performance_summary.png
```

---

## Local ArmoniK Configuration

Set the config path before running ArmoniK scripts:

```bash
export AKCONFIG=/home/ywang/ArmoniK/infrastructure/quick-deploy/localhost/generate
```

The local scripts currently use:

```python
endpoint  = "172.25.249.249:5001"
partition = "pymonik"
```

> ⚠️ These values may need to be updated depending on your local ArmoniK deployment.
