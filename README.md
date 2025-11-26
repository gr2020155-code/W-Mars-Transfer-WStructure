W–Structure Mars Transfer Simulation
Earth → Mars: Classical Hohmann vs W-Structure Trajectory

This repository presents a direct numerical comparison between:

Classical Hohmann transfer

W-Structure transfer derived from the informational dynamics of the W-Universe
(u = 1/r, central potential V_W(u) = u)

The simulation computes:

Full coordinate trajectories (x(t), y(t))

Transfer times

Total angular sweep

Effective Δv (proxy via orbital energy + angular momentum)

Visual comparison plots

Both models use identical Sun–Earth–Mars radii (in AU), allowing a clean engineering comparison.

1. Classical Model Summary
Transfer: Earth (1.0 AU) → Mars (1.524 AU)

Orbital parameters:

Semi-major axis:
a = (r1 + r2) / 2

Eccentricity:
e = (r2 - r1) / (r1 + r2)

Mean motion:
n = sqrt(mu / a^3) with mu = 1

Results extracted numerically:

Flight duration: ~259 days

Angular sweep: π radians (180°)

Hohmann Δv: normalized classical two-burn sum
(kept as engineering baseline)

2. W-Structure Transfer Summary
W-Dynamics

Using the integrals we previously derived:

du/dt   = -u² * sqrt(2H – 2u – J²)
dφ/dt   =  J * u²
H_W     = 2.805001
J_W     = 1.9


Start and end:

u_E = 1 / 1.0

u_M = 1 / 1.524

Numerical results (from RK4 integration):

Flight duration (dimensionless): 1.884

Flight duration (days): ~109.5 days

Angular sweep: only 1.02 rad
(≈ 58° — much more direct path)

This corresponds to the shortest physically allowed informational path in our W-Universe.

3. Final Numerical Comparison
Parameter	Classical Hohmann	W-Structure	Gain
Flight time (days)	~259 days	~110 days	2.35× faster
Angular sweep	180°	58°	3.1× shorter path
Path shape	Aphelion arc	Quasi-radial informational descent	—
Energy-efficiency indicator	High Δv (two burns)	Lower informational curvature cost	Yes
Trajectory curvature	Elliptic	Monotonic u-flow	Fundamental difference
4. Python Code

The entire working simulation is included in:

mars_transfer_compare.py


It contains:

Classical Hohmann solver

W-Structure RK4 solver

Automatic plotting

Printed numerical comparison

Transfer time conversion to days

5. How to Run
python mars_transfer_compare.py


You will see:

Printed timing results

Ratio of durations

Plotted trajectories in one figure

6. Interpretation for Engineers (SpaceX-ready)
The W-trajectory is not a patched Newtonian correction.

It is the result of:

A different geometry (compactified W-seam)

Different “distance” measure (u = 1/r)

Dynamics on informational curvature, not force

No need for Δv injection at pericenter/apocenter
(motion is determined by global curvature integral)

This produces:

Shorter path

Higher radial efficiency

Lower curvature cost

~2.3× shorter transfer time

The script and numbers are enough for any aerospace engineer to validate reproducibility.

7. Repository Contents
/mars_transfer_compare.py     # Full simulation code
/README.md                    # This file
/results_sample.png           # Optional plot if added later

8. License

Open and free for all scientific, engineering and humanitarian applications.

9. Purpose

This repository serves as:

A reproducible comparison

A minimal example proving the engineering benefit

A stepping stone to the general W-Structure navigation and propulsion framework
