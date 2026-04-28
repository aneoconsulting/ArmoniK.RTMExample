# ArmoniK RTM Example

This repository contains small experimental workflows connecting ArmoniK with inverse problems and SEM3D outputs.

## Contents

- `experiments/mini_inverse_case/`: toy inverse problem with ArmoniK batching and task-granularity analysis.
- `experiments/sem3d_inverse_case/`: SEM3D HDF5 trace reading, misfit computation, ArmoniK batch processing, and visualization.

## Main idea

The project starts from a simplified inverse problem, studies ArmoniK task granularity, and then progressively connects the workflow to real SEM3D output traces.

## Key result

Batching is important in ArmoniK workflows. Very small tasks create high scheduling overhead, while batched tasks reduce execution time without changing the numerical result.
