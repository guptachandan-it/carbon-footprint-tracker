# Carbon Footprint Tracker (CarbonKind)

An academic Idea Lab-3 web platform for estimating monthly emissions from electricity, transportation, and household waste. Results are estimates only, based on configurable demonstration factors.

## Features

- Multi-entry transport calculator with server-side validation
- Plotly category, comparison, and historical charts
- SQLite assessment storage, detail pages, sorting, deletion, and comparison
- Responsive Flask, HTML, CSS, and JavaScript interface

## Stack

Python, Flask, Pandas, SQLite, HTML/CSS/JavaScript, and Plotly.js.

## Install and run

```bash
python -m venv venv
source venv/bin/activate       # macOS/Linux
# Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Open http://127.0.0.1:5000. The SQLite database is created automatically. Optional sample records can be made with `python seed_demo.py`.

## Calculation approach

Electricity = kWh × electricity factor. Transportation = sum(distance × mode factor). Waste = kg × waste factor. Total is their sum, in kg CO2e/month (tonnes = kg / 1000). Factors live in `data/emission_factors.json` and are configurable academic demonstration estimates, not universally precise measurements.

## API routes

`GET /api/history`, `GET /api/assessment/<id>`; primary pages include `/`, `/calculate`, `/dashboard`, `/history`, `/assessment/<id>`, and `/about`.

## Academic subject mapping

ADSA: lists and sorting; DBMS: SQLite CRUD; Discrete Mathematics: functions; Automata Theory: input-to-result validation flow; Environmental Studies: emissions and sustainable practices.

## Limitations and future work

No authentication or region-specific factors are included. Future work could add user accounts, factor sources by location, exports, and more activity categories.

## Screenshots

Add project screenshots here for the final presentation.
