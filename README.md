# Heat Transfer Analyser

A Streamlit web app for PE 262 (Computer Programming for Petroleum Engineers,
KNUST) Project 8 — Vibe Coding Mini-App. The app has two interactive modes,
selectable from the sidebar: **steady-state conduction** through a flat wall
(Fourier's Law) and **Newton's Law of Cooling** (time to reach a target
temperature, with a full cooling curve). Each mode has live sliders/inputs,
metric cards, a colour-coded status line, a Matplotlib chart, and a Pandas
results table.

**Live app:** _add your Streamlit Community Cloud URL here after deploying_

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

See the comment block at the top of `app.py` for the AI tool used, key
prompts, and what was manually verified/corrected.
