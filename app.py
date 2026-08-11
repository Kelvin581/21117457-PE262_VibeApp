"""
Heat Transfer Analyser — PE 262 Project 8 (Vibe Coding Mini-App)
"""

import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

# ----------------------------------------------------------------
# PAGE SETUP
# ----------------------------------------------------------------
st.set_page_config(page_title="Heat Transfer Analyser", layout="wide")
st.title("Heat Transfer Analyser")
st.markdown(
    "Steady-state conduction (Fourier's Law) and transient cooling "
    "(Newton's Law of Cooling) in one tool. Adjust the inputs in the "
    "sidebar — results, charts, and a data table update instantly."
)

# ----------------------------------------------------------------
# ENGINEERING FUNCTIONS (verified against hand calculations)
# ----------------------------------------------------------------
def conduction_flux(k, L, T_H, T_C):
    """
    Steady-state 1D conduction heat flux through a flat wall (Fourier's Law).

    Parameters:
        k   (float): thermal conductivity, W/(m*K)
        L   (float): wall thickness, m
        T_H (float): hot-side temperature, deg C
        T_C (float): cold-side temperature, deg C

    Returns:
        float: heat flux q, W/m^2

    Raises:
        ValueError: if k <= 0 or L <= 0
    """
    if k <= 0:
        raise ValueError(f"Thermal conductivity must be > 0, got {k}")
    if L <= 0:
        raise ValueError(f"Wall thickness must be > 0, got {L}")
    return k * (T_H - T_C) / L


def cooling_time(T0, T_inf, T_target, k):
    """
    Time for an object to cool (or warm) from T0 to T_target in an
    ambient environment T_inf, via Newton's Law of Cooling:
        T(t) = T_inf + (T0 - T_inf) * exp(-k*t)

    Parameters:
        T0       (float): initial temperature, deg C
        T_inf    (float): ambient temperature, deg C
        T_target (float): target temperature, deg C
        k        (float): cooling constant, per minute

    Returns:
        float: time in minutes to reach T_target

    Raises:
        ValueError: if k <= 0, or T_target is not strictly between
                    T_inf and T0 (required for the log to be defined
                    and physically meaningful)
    """
    if k <= 0:
        raise ValueError(f"Cooling constant k must be > 0, got {k}")
    lo, hi = sorted([T_inf, T0])
    if not (lo < T_target < hi):
        raise ValueError(
            f"T_target ({T_target}) must be strictly between "
            f"T_inf ({T_inf}) and T0 ({T0})"
        )
    return -math.log((T_target - T_inf) / (T0 - T_inf)) / k


def cooling_curve(T0, T_inf, k, t_max, n=200):
    """
    Generate a temperature-vs-time array for plotting the cooling curve.

    Parameters:
        T0    (float): initial temperature, deg C
        T_inf (float): ambient temperature, deg C
        k     (float): cooling constant, per minute
        t_max (float): maximum time to plot, minutes
        n     (int)  : number of points

    Returns:
        (np.ndarray, np.ndarray): time array (min), temperature array (degC)
    """
    t = np.linspace(0, t_max, n)
    T = T_inf + (T0 - T_inf) * np.exp(-k * t)
    return t, T


# ----------------------------------------------------------------
# SIDEBAR — MODE SELECTOR + INPUTS
# ----------------------------------------------------------------
st.sidebar.header("Analysis Mode")
mode = st.sidebar.radio("Select calculation:", ["Conduction", "Cooling Curve"])

st.sidebar.header("Inputs")

if mode == "Conduction":
    k = st.sidebar.number_input(
        "Thermal conductivity k (W/m·K)", value=50.0, min_value=0.01, format="%.2f"
    )
    L_mm = st.sidebar.slider("Wall thickness L (mm)", 10, 500, 100)
    L = L_mm / 1000
    T_H = st.sidebar.slider("Hot-side temperature T_H (°C)", 0, 1000, 500)
    T_C = st.sidebar.slider("Cold-side temperature T_C (°C)", -50, 500, 100)
    area = st.sidebar.number_input(
        "Wall area (m²)", value=1.0, min_value=0.01, format="%.2f"
    )
else:
    T0 = st.sidebar.slider("Initial temperature T0 (°C)", 0, 1000, 600)
    T_inf = st.sidebar.slider("Ambient temperature T_inf (°C)", -20, 100, 25)
    k_cool = st.sidebar.number_input(
        "Cooling constant k (1/min)", value=0.02, min_value=0.0001, format="%.4f"
    )
    T_target = st.sidebar.slider(
        "Target temperature (°C)", int(min(T0, T_inf)) + 1, int(max(T0, T_inf)) - 1, 50
    )

# ----------------------------------------------------------------
# MAIN AREA — CONDUCTION MODE
# ----------------------------------------------------------------
if mode == "Conduction":
    try:
        q = conduction_flux(k, L, T_H, T_C)
        Q_total = q * area

        col1, col2, col3 = st.columns(3)
        col1.metric("Heat Flux", f"{q:,.1f} W/m²")
        col2.metric("Total Heat Rate", f"{Q_total:,.1f} W")
        col3.metric("ΔT", f"{T_H - T_C:.1f} °C")

        colour = "green" if q < 500 else ("orange" if q < 2000 else "red")
        level = "Low" if q < 500 else ("Moderate" if q < 2000 else "High")
        st.markdown(
            f'<h3 style="color:{colour}">Flux Level: {level}</h3>',
            unsafe_allow_html=True,
        )

        # Two-panel sweep chart: flux vs L, and flux vs T_H
        L_range_mm = np.linspace(10, 500, 100)
        q_vs_L = [conduction_flux(k, l / 1000, T_H, T_C) for l in L_range_mm]

        T_H_range = np.linspace(0, 1000, 100)
        q_vs_TH = [conduction_flux(k, L, th, T_C) for th in T_H_range]

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.5))

        ax1.plot(L_range_mm, q_vs_L, "b-", lw=2)
        ax1.axvline(L_mm, color="red", ls="--", label=f"Current L = {L_mm} mm")
        ax1.set_xlabel("Wall Thickness (mm)")
        ax1.set_ylabel("Heat Flux (W/m²)")
        ax1.set_title("Flux vs Wall Thickness")
        ax1.legend()
        ax1.grid(True, alpha=0.4)

        ax2.plot(T_H_range, q_vs_TH, "g-", lw=2)
        ax2.axvline(T_H, color="red", ls="--", label=f"Current T_H = {T_H} °C")
        ax2.set_xlabel("Hot-Side Temperature (°C)")
        ax2.set_ylabel("Heat Flux (W/m²)")
        ax2.set_title("Flux vs Hot-Side Temperature")
        ax2.legend()
        ax2.grid(True, alpha=0.4)

        plt.tight_layout()
        st.pyplot(fig)

        # Results table across a few wall thicknesses
        st.subheader("Comparison Table — Flux at Different Wall Thicknesses")
        thick_list = [10, 25, 50, 100, 200, 500]
        table_rows = []
        for t_mm in thick_list:
            q_t = conduction_flux(k, t_mm / 1000, T_H, T_C)
            table_rows.append({
                "Thickness (mm)": t_mm,
                "Flux (W/m²)": round(q_t, 1),
                "Total Heat Rate (W)": round(q_t * area, 1),
            })
        df_table = pd.DataFrame(table_rows)
        st.dataframe(df_table, use_container_width=True)

    except ValueError as e:
        st.warning(f"Input error: {e}")

# ----------------------------------------------------------------
# MAIN AREA — COOLING CURVE MODE
# ----------------------------------------------------------------
else:
    try:
        t_target = cooling_time(T0, T_inf, T_target, k_cool)

        col1, col2, col3 = st.columns(3)
        col1.metric("Time to Target", f"{t_target:,.1f} min")
        col2.metric("Target Temperature", f"{T_target:.1f} °C")
        col3.metric("Temperature Drop", f"{T0 - T_target:.1f} °C")

        colour = "green" if t_target < 60 else ("orange" if t_target < 180 else "red")
        speed = "Fast" if t_target < 60 else ("Moderate" if t_target < 180 else "Slow")
        st.markdown(
            f'<h3 style="color:{colour}">Cooling Speed: {speed}</h3>',
            unsafe_allow_html=True,
        )

        t_arr, T_arr = cooling_curve(T0, T_inf, k_cool, t_max=t_target * 1.3)

        fig, ax = plt.subplots(figsize=(9, 4.5))
        ax.plot(t_arr, T_arr, "b-", lw=2, label="Temperature")
        ax.axhline(T_target, color="green", ls="--", label=f"Target = {T_target} °C")
        ax.axvline(t_target, color="red", ls="--", label=f"t = {t_target:.1f} min")
        ax.set_xlabel("Time (min)")
        ax.set_ylabel("Temperature (°C)")
        ax.set_title("Newton's Law of Cooling — Temperature vs Time")
        ax.legend()
        ax.grid(True, alpha=0.4)
        st.pyplot(fig)

        # Results table at fixed time intervals
        st.subheader("Temperature at Time Intervals")
        n_steps = 8
        t_checkpoints = np.linspace(0, t_target * 1.3, n_steps)
        table_rows = []
        for t_val in t_checkpoints:
            T_val = T_inf + (T0 - T_inf) * math.exp(-k_cool * t_val)
            table_rows.append({
                "Time (min)": round(t_val, 1),
                "Temperature (°C)": round(T_val, 1),
            })
        df_table = pd.DataFrame(table_rows)
        st.dataframe(df_table, use_container_width=True)

    except ValueError as e:
        st.warning(f"Input error: {e}")

st.markdown("---")
st.caption("PE 262 · Project 8 · Vibe Coding Mini-App · Built with Streamlit + AI assistance")
