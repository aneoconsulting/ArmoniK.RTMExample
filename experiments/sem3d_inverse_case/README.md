# SEM3D Inverse Case with ArmoniK

This experiment extends the toy inverse problem to **real SEM3D outputs**.

Instead of using an analytical forward model, we work directly with **SEM3D simulation traces stored in HDF5 format** to compute misfit values between traces.

---

## Objective

Validate the following end-to-end pipeline:

```
SEM3D outputs → trace extraction → misfit computation → ArmoniK batch processing → visualization
```

---

## Data

The experiment uses SEM3D receiver outputs located at:

```
templates/traces/capteurs.*.h5
```

Each HDF5 file contains multiple stations (`UU_0000`, `UU_0001`, ...), each with time series for:
- Displacement
- Velocity
- Acceleration

---

## Workflow Steps

### Step 6C — Read SEM3D Traces and Compute Misfit

**Script:** `step6c_sem3d_trace_misfit.py`

- Reads SEM3D HDF5 trace files
- Automatically detects available stations
- Extracts a specific component (e.g. `Displ 1`)
- Computes misfit between two signals

**Validates that:**
- The HDF5 structure is correctly understood
- Station traces can be extracted
- Misfit computation is consistent

---

### Step 6D — ArmoniK Batch Misfit Computation

**Script:** `step6d_armonik_sem3d_trace_misfit.py`

- Reads all station traces locally
- Sends extracted NumPy arrays to ArmoniK tasks
- Each task processes a batch of traces in parallel
- Aggregates and sorts results

> ⚠️ **Note:** ArmoniK workers cannot access local file paths directly.  
> Data must be loaded locally and serialized before being sent to tasks.

---

### Step 6E — Visualization

**Script:** `step6e_sem3d_armonik_visualization.py`

Generates the following plots to analyze misfit structure:

| Plot | Insight |
|---|---|
| Top 10 closest station traces (bar plot) | Similarity between station responses |
| Misfit distribution (histogram) | Spread of misfit values |
| Sorted misfit curve | Presence of clusters or outliers |

---

## Key Insights

- SEM3D outputs are distributed across multiple HDF5 files (parallel simulation output)
- Stations must be reconstructed across files
- Misfit computation applies directly on raw traces
- ArmoniK batching significantly simplifies parallel processing

---

