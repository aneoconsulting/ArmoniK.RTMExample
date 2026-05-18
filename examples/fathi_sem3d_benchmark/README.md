# SEM3D Fathi et al. 2015 Benchmark

This project aims to reproduce a simplified benchmark inspired by:

Fathi et al. (2015), "Full-waveform inversion in three-dimensional PML-truncated elastic media".

The objective is to build a SEM3D benchmark workflow for RTM / FWI preparation.

## General workflow

Target model
→ SEM3D forward simulation
→ observed receiver data

Initial model
→ SEM3D forward simulation
→ simulated receiver data

Observed data vs simulated data
→ receiver trace misfit
→ residual construction
→ future adjoint / RTM workflow

## Selected benchmark case

We start from the layered medium case in Fathi et al. 2015.

The computational domain is approximately(4.3 Layered medium):

- Length: 40 m
- Width: 40 m
- Depth: 45 m
- PML thickness: 6.25 m

The target material model is a three-layer elastic medium:

lambda(z) = mu(z) =

- 80 MPa for -12 m <= z <= 0 m
- 101.25 MPa for -27 m <= z < -12 m
- 125 MPa for -50 m <= z < -27 m

Density:

- rho = 2000 kg/m^3

## Important note

This first stage does not implement the full adjoint method yet.

Current goal:

- construct the benchmark geometry
- generate target and initial material models
- run SEM3D forward simulations
- compute receiver trace misfit

Future goal:

- construct adjoint source from residual traces
- perform backward / adjoint simulation
- compute RTM imaging condition or material gradients
