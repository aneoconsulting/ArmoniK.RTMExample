# Fathi et al. 2015 layered medium benchmark parameters

## Target model

The target model is a horizontally layered elastic medium.

Domain:

- x direction: 40 m
- y direction: 40 m
- z direction: 45 m depth
- PML thickness: 6.25 m

Material parameters:

| Depth range | lambda | mu | density |
|---|---:|---:|---:|
| -12 m <= z <= 0 m | 80 MPa | 80 MPa | 2000 kg/m^3 |
| -27 m <= z < -12 m | 101.25 MPa | 101.25 MPa | 2000 kg/m^3 |
| -50 m <= z < -27 m | 125 MPa | 125 MPa | 2000 kg/m^3 |

In SI units:

- 80 MPa = 80e6 Pa
- 101.25 MPa = 101.25e6 Pa
- 125 MPa = 125e6 Pa

## Initial model

The first initial model will be homogeneous:

- lambda = 80 MPa
- mu = 80 MPa
- rho = 2000 kg/m^3

## Receiver misfit

The receiver trace misfit will be computed as:

J = 1/2 * sum_j integral_0^T ||u_sim(x_j,t) - u_obs(x_j,t)||^2 dt

where:

- u_obs is generated from the target model
- u_sim is generated from the initial model
- x_j are receiver positions on the surface

## Current stage

This is only the benchmark preparation stage.

We first build:

1. target material model
2. initial material model
3. forward simulations
4. receiver trace comparison
5. misfit calculation

Adjoint simulation and true gradient update will be addressed later.
