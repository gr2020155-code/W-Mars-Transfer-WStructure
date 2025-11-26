#!/usr/bin/env python3
"""
Earth→Mars transfer comparison:
- Classical Hohmann transfer (Newtonian, mu=1)
- W-Structure transfer (u = 1/r, H_W≈2.805, J_W≈1.9)

Outputs:
- Transfer times (dimensionless + days)
- Δv_classic (km/s units for r=1 AU normalized model)
- Δv_W (engineering estimate)
- Saves trajectory.png
"""

import numpy as np
import math
import matplotlib.pyplot as plt

# ---------------- Common parameters ----------------
MU = 1.0          # gravitational parameter (normalized)
R_E = 1.0         # Earth orbit radius (AU)
R_M = 1.524       # Mars orbit radius (AU)
U_E = 1.0
U_M = 1.0 / R_M

YEAR = 2 * math.pi
DAY_PER_UNIT = 365.25 / YEAR


# ============================================================
# 1. Classical Hohmann Transfer
# ============================================================

def hohmann_transfer():
    r1 = R_E
    r2 = R_M

    # ellipse parameters
    a_t = 0.5 * (r1 + r2)
    e_t = (r2 - r1) / (r2 + r1)
    n_t = math.sqrt(MU / a_t**3)

    NE = 500
    E_arr = np.linspace(0, math.pi, NE)
    M_arr = E_arr - e_t * np.sin(E_arr)

    t_arr = M_arr / n_t
    t_arr -= t_arr[0]

    r_arr = a_t * (1 - e_t * np.cos(E_arr))
    cos_f = (np.cos(E_arr) - e_t) / (1 - e_t * np.cos(E_arr))
    sin_f = (np.sqrt(1 - e_t**2) * np.sin(E_arr)) / (1 - e_t * np.cos(E_arr))
    f_arr = np.arctan2(sin_f, cos_f)

    x_arr = r_arr * np.cos(f_arr)
    y_arr = r_arr * np.sin(f_arr)

    # ------ Δv classical ------
    v1 = math.sqrt(MU / r1)
    v2 = math.sqrt(MU / r2)
    v_peri = math.sqrt(MU * (2/r1 - 1/a_t))
    v_apo  = math.sqrt(MU * (2/r2 - 1/a_t))

    dv1 = abs(v_peri - v1)
    dv2 = abs(v2 - v_apo)
    dv_total = dv1 + dv2

    return {
        "t": t_arr,
        "x": x_arr,
        "y": y_arr,
        "T": t_arr[-1],
        "Δv": dv_total
    }


# ============================================================
# 2. W-Structure Transfer
# ============================================================

H_W = 2.805001
J_W = 1.9

def integrate_W(dt=1e-3):
    t = 0.0
    u = U_E
    phi = 0.0

    T_list, u_list, phi_list = [t], [u], [phi]

    def f_u(u):
        rad = 2*H_W - 2*u - J_W**2
        if rad < 0: return 0
        return -u*u * math.sqrt(rad)

    def f_phi(u):
        return J_W * u*u

    while u > U_M:
        k1_u = f_u(u)
        k2_u = f_u(u + 0.5*dt*k1_u)
        k3_u = f_u(u + 0.5*dt*k2_u)
        k4_u = f_u(u + dt*k3_u)

        k1_p = f_phi(u)
        k2_p = f_phi(u + 0.5*dt*k1_u)
        k3_p = f_phi(u + 0.5*dt*k2_u)
        k4_p = f_phi(u + dt*k3_u)

        u += (dt/6)*(k1_u + 2*k2_u + 2*k3_u + k4_u)
        phi += (dt/6)*(k1_p + 2*k2_p + 2*k3_p + k4_p)
        t += dt

        T_list.append(t)
        u_list.append(u)
        phi_list.append(phi)

        if t > 10:
            break

    t = np.array(T_list)
    u = np.array(u_list)
    phi = np.array(phi_list)

    r = 1/u
    x = r * np.cos(phi)
    y = r * np.sin(phi)

    # --- Engineering Δv estimate ---
    du_dt0 = f_u(U_E)
    local_rad = max(2*H_W - 2*U_E - J_W**2, 0)
    effective_energy_shift = math.sqrt(local_rad)
    dv_W = effective_energy_shift

    return {
        "t": t,
        "x": x,
        "y": y,
        "T": t[-1],
        "Δv": dv_W
    }


# ============================================================
# 3. Plot + output
# ============================================================

def main():
    hoh = hohmann_transfer()
    w = integrate_W()

    days_classic = hoh["T"] * DAY_PER_UNIT
    days_W = w["T"] * DAY_PER_UNIT

    print("\n=== Transfer Times ===")
    print(f"Classic Hohmann : {days_classic:.1f} days")
    print(f"W-Structure     : {days_W:.1f} days")
    print(f"Ratio T_W/T_classic = {w['T']/hoh['T']:.3f}")

    print("\n=== Delta-V ===")
    print(f"Δv_classic = {hoh['Δv']:.4f} (normalized units)")
    print(f"Δv_W       = {w['Δv']:.4f} (engineering estimate)")
    print(f"Δv ratio   = {w['Δv']/hoh['Δv']:.3f}")

    # ----- Plot -----
    plt.figure(figsize=(7,7))
    plt.plot(hoh["x"], hoh["y"], '--', label="Hohmann")
    plt.plot(w["x"], w["y"], label="W-Structure")

    th = np.linspace(0, 2*np.pi, 800)
    plt.plot(R_E*np.cos(th), R_E*np.sin(th), color="gray", alpha=0.5)
    plt.plot(R_M*np.cos(th), R_M*np.sin(th), color="red", alpha=0.3)

    plt.gca().set_aspect("equal")
    plt.grid(True)
    plt.legend()
    plt.title("Earth→Mars: Classical vs W-Structure")
    plt.tight_layout()
    plt.savefig("trajectory.png", dpi=200)

    print("\nSaved: trajectory.png")


if __name__ == "__main__":
    main()
