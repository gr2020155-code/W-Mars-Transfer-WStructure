import numpy as np
import math
import matplotlib.pyplot as plt

MU = 1.0
R_E = 1.0
R_M = 1.524
U_E = 1.0
U_M = 1.0 / R_M

YEAR_IN_UNITS = 2.0 * math.pi
TIME_UNIT_DAYS = 365.25 / YEAR_IN_UNITS

def hohmann_transfer():
    r1 = R_E
    r2 = R_M
    a_t = 0.5 * (r1 + r2)
    e_t = (r2 - r1) / (r2 + r1)
    n_t = math.sqrt(MU / a_t**3)

    E_arr = np.linspace(0.0, math.pi, 400)
    r_arr = a_t * (1.0 - e_t * np.cos(E_arr))
    cos_f = (np.cos(E_arr) - e_t) / (1.0 - e_t * np.cos(E_arr))
    sin_f = (np.sqrt(1.0 - e_t**2) * np.sin(E_arr)) / (1.0 - e_t * np.cos(E_arr))
    f_arr = np.arctan2(sin_f, cos_f)
    M_arr = E_arr - e_t * np.sin(E_arr)
    t_arr = M_arr / n_t
    t_arr -= t_arr[0]

    x_arr = r_arr * np.cos(f_arr)
    y_arr = r_arr * np.sin(f_arr)

    return {"t": t_arr, "x": x_arr, "y": y_arr, "T": t_arr[-1]}

H_W = 2.805001
J_W = 1.9

def integrate_W_transfer(dt=1e-3):
    t = 0.0
    u = U_E
    phi = 0.0

    t_list = [t]
    u_list = [u]
    phi_list = [phi]

    while u > U_M:
        rad = 2.0 * H_W - 2.0 * u - J_W**2
        if rad < 0:
            break

        du = -u**2 * math.sqrt(rad)
        dphi = J_W * u**2

        u2 = u + 0.5 * dt * du
        rad2 = 2.0 * H_W - 2.0 * u2 - J_W**2
        du2 = -u2**2 * math.sqrt(max(rad2,0))
        dphi2 = J_W * (u2**2)

        u3 = u + 0.5 * dt * du2
        rad3 = 2.0 * H_W - 2.0 * u3 - J_W**2
        du3 = -u3**2 * math.sqrt(max(rad3,0))
        dphi3 = J_W * (u3**2)

        u4 = u + dt * du3
        rad4 = 2.0 * H_W - 2.0 * u4 - J_W**2
        du4 = -u4**2 * math.sqrt(max(rad4,0))
        dphi4 = J_W * (u4**2)

        u += (dt/6.0)*(du + 2*du2 + 2*du3 + du4)
        phi += (dt/6.0)*(dphi + 2*dphi2 + 2*dphi3 + dphi4)
        t += dt

        t_list.append(t)
        u_list.append(u)
        phi_list.append(phi)

        if t > 10.0:
            break

    t_arr = np.array(t_list)
    u_arr = np.array(u_list)
    phi_arr = np.array(phi_list)
    r_arr = 1.0 / u_arr

    x_arr = r_arr * np.cos(phi_arr)
    y_arr = r_arr * np.sin(phi_arr)

    return {"t": t_arr, "x": x_arr, "y": y_arr, "T": t_arr[-1]}

def main():
    hoh = hohmann_transfer()
    T_classic = hoh["T"]
    days_classic = T_classic * TIME_UNIT_DAYS

    w = integrate_W_transfer()
    T_W = w["T"]
    days_W = T_W * TIME_UNIT_DAYS

    print("=== Classical Hohmann Transfer ===")
    print(f"T_classic = {days_classic:.2f} days")
    print("=== W-Structure Transfer ===")
    print(f"T_W       = {days_W:.2f} days")
    print(f"Ratio T_W / T_classic = {T_W/T_classic:.3f}")

    plt.figure(figsize=(7,7))
    plt.plot(hoh["x"], hoh["y"], "--", label="Hohmann")
    plt.plot(w["x"], w["y"], label="W-Structure")

    theta = np.linspace(0, 2*math.pi, 400)
    plt.plot(R_E*np.cos(theta), R_E*np.sin(theta), "gray", alpha=0.4)
    plt.plot(R_M*np.cos(theta), R_M*np.sin(theta), "red", alpha=0.3)

    plt.gca().set_aspect("equal")
    plt.grid(True)
    plt.legend()
    plt.show()

if __name__ == "__main__":
    main()
