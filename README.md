# Heat Transfer Analyser

A Streamlit web app for PE 262 (Computer Programming for Petroleum Engineers,
KNUST) Project 8 — Vibe Coding Mini-App. The app has two interactive modes,
selectable from the sidebar: **steady-state conduction** through a flat wall
(Fourier's Law) and **Newton's Law of Cooling** (time to reach a target
temperature, with a full cooling curve). Each mode has live sliders/inputs,
metric cards, a colour-coded status line, a Matplotlib chart, and a Pandas
results table.

**Live app:** <https://kelvin-eng-dash.streamlit.app/>

## Running locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Modes

- **Conduction:** enter thermal conductivity, wall thickness, hot/cold-side
  temperatures, and wall area. Returns heat flux (W/m²) and total heat rate
  (W), plus a two-panel chart showing flux sensitivity to wall thickness and
  hot-side temperature, and a table comparing flux across wall thicknesses.
- **Cooling Curve:** enter initial/ambient/target temperatures and a cooling
  constant. Returns time to reach the target temperature, plus the full
  T(t) cooling curve and a table of temperature at fixed time intervals.

All formulas were verified by hand against the worked examples in the PE 262
course notes (Week 1 Example 1.4, Week 3 while-loop exercise) before being
used in this app.

## AI usage disclosure

==================================================================

AI TOOLS USED: Claude (Anthropic)

KEY PROMPTS USED (summarised — see project submission for full log):
1. "Build a Streamlit app with two modes selectable via a sidebar radio:
   (a) steady-state conduction through a flat wall using Fourier's Law,
   (b) Newton's Law of Cooling time-to-target. Follow the Week 8.2 course
   pattern: sidebar inputs, st.columns metrics, colour-coded status line,
   one Matplotlib figure with st.pyplot(fig)."
2. "For the conduction mode, add a two-panel chart: flux vs wall thickness
   (sweeping L) and flux vs hot-side temperature (sweeping T_H), each
   marking the current operating point with axvline."
3. "Add input validation (k<=0, L<=0, T_target outside [T_inf, T0], etc.)
   that shows st.warning() instead of crashing, matching the try/except
   pattern used in Week 4 and Week 7 of the course."

 ## WHAT I HAD TO MANUALLY VERIFY / FIX:
The cooling-time formula t = -ln((T_target - T_inf)/(T0 - T_inf)) / k only
holds when T_inf < T_target < T0 (or the reverse order for heating). The
first AI draft did not guard this and would silently return a negative or
complex-valued nonsense time if T_target was entered outside that range
(e.g. below ambient). I added an explicit range check that raises
ValueError with a clear message before the log is evaluated. I verified
the corrected formula by hand against the Week 3 worked example
(T0=600, T_inf=25, k=0.02, T_target=50 -> t=157.0 min) and against the
Week 1 Example 1.4 result (t=157 min) before trusting the app's output.

AI TOOLS USED: Claude (Anthropic)

KEY PROMPTS USED (summarised — see project submission for full log):
1. "Build a Streamlit app with two modes selectable via a sidebar radio:
   (a) steady-state conduction through a flat wall using Fourier's Law,
   (b) Newton's Law of Cooling time-to-target. Follow the Week 8.2 course
   pattern: sidebar inputs, st.columns metrics, colour-coded status line,
   one Matplotlib figure with st.pyplot(fig)."
2. "For the conduction mode, add a two-panel chart: flux vs wall thickness
   (sweeping L) and flux vs hot-side temperature (sweeping T_H), each
   marking the current operating point with axvline."
3. "Add input validation (k<=0, L<=0, T_target outside [T_inf, T0], etc.)
   that shows st.warning() instead of crashing, matching the try/except
   pattern used in Week 4 and Week 7 of the course."

## WHAT I HAD TO MANUALLY VERIFY / FIX:

The cooling-time formula t = -ln((T_target - T_inf)/(T0 - T_inf)) / k only
holds when T_inf < T_target < T0 (or the reverse order for heating). The
first AI draft did not guard this and would silently return a negative or
complex-valued nonsense time if T_target was entered outside that range
(e.g. below ambient). I added an explicit range check that raises
ValueError with a clear message before the log is evaluated. I verified
the corrected formula by hand against the Week 3 worked example
(T0=600, T_inf=25, k=0.02, T_target=50 -> t=157.0 min) and against the
Week 1 Example 1.4 result (t=157 min) before trusting the app's output.
==================================================================
