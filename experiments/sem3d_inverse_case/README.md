# SEM3D Inverse Case with ArmoniK

This experiment extends the toy inverse problem workflow to real SEM3D outputs.

Instead of using an analytical forward model, we work directly with SEM3D receiver traces stored in HDF5 format. The goal is to validate the data-handling and parallel misfit-computation pipeline before launching new SEM3D simulations directly from ArmoniK tasks.

---

## Objective

Validate the following workflow:

```text
SEM3D HDF5 outputs
→ trace extraction
→ misfit computation
→ ArmoniK batch processing
→ result aggregation
```

This is an intermediate step toward a fully coupled HPC inversion workflow.

---

## ⚠️ Important Clarification

This experiment does **not** perform a full SEM3D inversion.

It validates the data pipeline on **existing** SEM3D outputs — no new simulations are launched from ArmoniK tasks. The misfit computation is used to confirm that trace reading, serialization, batch processing, and result aggregation work correctly end-to-end.

A full inversion loop (ArmoniK → SEM3D solver → misfit → optimization) is the planned next step.

---

## Data

The experiment uses SEM3D receiver outputs located at:

```
templates/traces/capteurs.*.h5
```

The `capteurs.*.h5` files are distributed outputs of the **same** SEM3D simulation, not independent runs. Each file contains a subset of receiver stations (e.g. `UU_0000`, `UU_0001`, ...), storing time series for:

- Time
- Displacement components
- Velocity components
- Acceleration components

---

## Misfit Definition

In a full inversion setting, the misfit compares a simulated trace from a candidate model against an observed or reference trace, for the same station, component, and time window.

In this experiment, the misfit is used primarily to **validate the pipeline**: we compare extracted SEM3D traces to confirm that the full data path — reading, transfer, batch processing, and aggregation — works correctly.

---

## Workflow Steps

### Step 6C — Read SEM3D Traces and Compute Misfit

**Script:** `step6c_sem3d_trace_misfit.py`

- Reads SEM3D HDF5 trace files
- Automatically detects available stations
- Extracts a selected component (e.g. `Displ 1`)
- Computes a local misfit between two extracted traces
- Saves a test CSV and comparison plot

**Validates that:**
- The HDF5 structure is correctly understood
- Station traces can be extracted
- SEM3D variables (displacement, velocity, acceleration) are accessible
- Misfit computation works on real SEM3D trace data

---

### Step 6D — ArmoniK Batch Misfit Computation

**Script:** `step6d_armonik_sem3d_trace_misfit.py`

- Reads all SEM3D station traces locally
- Extracts NumPy arrays from HDF5 files
- Sends batches of trace arrays to ArmoniK tasks
- Computes misfits in parallel
- Aggregates and sorts results
- Saves the result table as CSV

> ⚠️ **Implementation note:** ArmoniK workers cannot access local WSL file paths directly.  
> HDF5 files are read locally first; only the extracted NumPy arrays are serialized and sent to tasks.

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

- SEM3D receiver outputs are distributed across multiple HDF5 files
- Each `capteurs.*.h5` contains only a subset of stations — names must be detected dynamically
- Misfit computation applies directly to extracted station traces
- ArmoniK can batch and parallelize misfit computation once data is available as NumPy arrays

---

## Current Status

This case validates:

```
real SEM3D output reading → trace extraction → misfit computation → ArmoniK batch processing
```

It does **not** yet launch new SEM3D simulations from ArmoniK tasks.

---

## Next Steps

The planned full inversion loop:

```
ArmoniK task
→ generate / modify SEM3D input files
→ launch SEM3D solver
→ read generated traces
→ compute misfit
→ return objective value
```

Further down the road, surrogate models and adjoint methods can be introduced to accelerate optimization and reduce the need for exhaustive parameter scans.
