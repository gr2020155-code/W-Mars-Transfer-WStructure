# W-Mars Transfer — W-Structure vs Classical Hohmann

This repository provides a minimal, reproducible engineering comparison between:

1. Classical Hohmann Earth→Mars transfer (Newtonian two-body).
2. W-Structure transfer derived from the informational potential V_W(u)=u, where u=1/r.

----

## Contents

- mars_sim.py — simulation script:
  * computes both transfers
  * prints transfer times
  * plots trajectories in (x,y)

----

## Key Results

- Earth orbit radius: 1.0 AU
- Mars orbit radius: 1.524 AU

Classical trajectory: standard Hohmann ellipse.

W-Structure trajectory: governed by the system (no line breaks):
    du/dt = -u^2 * sqrt(2*H_W - 2*u - J_W^2)
    dphi/dt = J_W * u^2
with parameters:
    H_W = 2.805001
    J_W = 1.9

Plot colors:
- Dashed blue: classical Hohmann ellipse
- Orange: W-Structure transfer
- Grey circle: Earth orbit
- Red circle: Mars orbit

----

## Installation (Windows PowerShell)

```bash
pip install numpy matplotlib
python mars_sim.py
Output
The script prints:

Classical transfer time (dimensionless + days)

W-Structure transfer time

Ratio T_W / T_classic

Then a plot opens showing both trajectories.

Purpose
This repository provides a single, clean, engineer-friendly demonstration of a W-Structure–based orbital transfer in comparison with a standard classical one.
It does not contain the full W-theory (geometry, algebra, Riemann program, informational cells, PAN principle, etc).
Those live in dedicated repositories.
Here we only show the practical effect: how a W-derived trajectory compares to a classical Hohmann transfer.


License

MIT License recommended (or choose your own).
---
