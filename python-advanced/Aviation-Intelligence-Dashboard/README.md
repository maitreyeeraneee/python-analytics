# ✈️ Aviation Intelligence Dashboard — Advanced Analytics & Delay Prediction

[![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-FF4B4B?style=flat&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Plotly](https://img.shields.io/badge/Plotly-Interactive-239B56?style=flat&logo=plotly&logoColor=white)](https://plotly.com/)
[![Folium](https://img.shields.io/badge/Folium-Maps-2E86C1?style=flat&logo=leaflet&logoColor=white)](https://python-visualization.github.io/folium/)
[![scikit-learn](https://img.shields.io/badge/scikit-learn-ML-1F77B4?style=flat&logo=scikit-learn&logoColor=white)](https://scikit-learn.org/)
[![Joblib](https://img.shields.io/badge/joblib-Model%20Artifacts-333333?style=flat&logo=python&logoColor=white)](https://joblib.readthedocs.io/)

> **Recruiter-ready portfolio project**: production-style Python analytics + an embedded ML prediction system for operational delay intelligence.

---

## 🧠 Project Overview
The **Aviation Intelligence Dashboard** is a modern Streamlit application that helps aviation operators, analysts, and decision-makers answer high-impact questions:
- **Which airlines and airports drive the most delays/cancellations?**
- **How have delay and cancellation patterns changed over time?**
- **Where do weather-related impacts show correlation with delay volume?**
- **What is the predicted arrival delay** given scenario-based operational inputs?

It combines:
- **Advanced operational analytics** (KPI cards, leaderboards, trend lines, heatmaps)
- **Interactive geospatial visualization** (Folium airport map)
- **An end-to-end ML system** (trained offline, used live in the dashboard)

---

## 🚀 Key Features
- 📊 **Operational KPIs** — flights, delays, cancellations, cancellation rate
- 🏆 **Airline intelligence** — delays leaderboard, cancellations leaderboard, market share
- 🛬 **Airport intelligence** — busiest vs. most delayed airports
- 📈 **Time intelligence** — yearly delay trends (sum/avg aggregation)
- 🌡️ **Heatmaps** — monthly × yearly delay/cancellation patterns
- 🌦️ **Weather delay insights** — weather delay trend + correlation analysis
- 🗺️ **Interactive airport map** — dataset-driven markers when `lat/lon` are available
- 🤖 **AI Flight Delay Prediction System** — live prediction using saved model artifacts
- 🔎 **Model interpretability** — feature importance visualization inside the dashboard

---

## 📈 Analytics Capabilities
### Airline Analytics
- **Top airlines by total arrival delay** (`arr_delay` aggregated by `carrier_name`)
- **Top airlines by total cancellations** (`arr_cancelled` aggregated by `carrier_name`)
- **Market share view** based on total flights per airline

### Airport Analytics
- **Busiest airports** by total arrival flights
- **Most delayed airports** by total arrival delays

### Trend & Heatmap Analytics
- **Yearly delay trend** — configurable aggregation (`sum` or `avg`)
- **Monthly × Year delay heatmap** — surfaces seasonality and operational volatility

### Cancellation Analytics
- **Cancellations by airline**
- **Cancellation time heatmap** — year × month patterns for operational planning

### Weather Delay Analytics
- **Weather delays over years** (from `weather_delay` if present, otherwise `weather_ct`)
- **Correlation heatmap** across numeric features to support root-cause exploration

---

## 🧠🤖 AI/ML Prediction System (Flight Delay)
The dashboard includes an embedded ML prediction engine that estimates **arrival delay (minutes)** from operational scenario inputs.

### Model Type
- **Algorithm**: `RandomForestRegressor`
- **Artifact**: `models/delay_prediction_model.pkl`

### Model Features (Training & Inference)
The model is trained using the following numeric inputs (feature order is enforced at inference time):
- `arr_flights`
- `carrier_ct`
- `weather_ct`
- `nas_ct`
- `security_ct`
- `late_aircraft_ct`

---

## 🖼️ Dashboard Screenshots
Add screenshots for the following UI sections to make your GitHub portfolio stand out:
- KPIs + filters
- Airline leaderboards
- Airport map
- Delay trend + heatmaps
- Weather insights
- ML prediction panel

---

## 🧾 KPI Highlights (Live Metrics)
Depending on the selected filters, the dashboard updates:
- **Total Flights** (sum of `arr_flights`)
- **Total Delays** (sum of `arr_delay`)
- **Cancelled Flights** (sum of `arr_cancelled`)
- **Cancellation Rate** (`arr_cancelled / arr_flights`)

---

## 🗺️ Interactive Maps (Airport Intelligence)
The dashboard renders an interactive **Folium** map embedded in Streamlit.
- Markers are created from airport-level rows
- The map is **dataset-driven**:
  - If the dataset contains `lat`/`lon` (or compatible column names like `latitude`/`longitude`), markers are shown
  - If lat/lon are missing, the app still loads with a safe default map view

---

## 🧰 Tech Stack
- **Python**
- **Streamlit** — dashboard UI
- **Plotly** — interactive charts
- **Folium + streamlit-folium** — map visualization
- **Pandas** — analytics + transformation
- **Seaborn** — supporting analysis scripts
- **scikit-learn** — model training (Random Forest)
- **joblib** — model artifact persistence

---

## 🏗️ Project Architecture
- `app.py`
  - Streamlit app orchestration
  - Data loading, sidebar filters, KPI + chart rendering
  - Embedded prediction UI
- `src/data.py`
  - `load_data()` for `dataset/flights.csv` (cached)
  - `apply_filters()` for year/airline/airport/month filtering
- `src/analytics.py`
  - KPI computation + aggregation logic
  - leaderboards, trends, cancellation analysis, weather analysis
- `src/charts.py`
  - Plotly figure generation
  - Folium map generation (`make_airport_map`)
- `src/prediction.py`
  - cached model loader
  - prediction wrapper and optional feature importance plotting
- `prediction_model.py`
  - offline training + artifact export

---

## 📁 Folder Structure
```text
Aviation-Intelligence-Dashboard/
  app.py
  prediction_model.py
  README.md
  requirements.txt
  TODO.md

  dataset/
    flights.csv

  models/
    delay_prediction_model.pkl

  plots/
    (generated plots & heatmaps)

  src/
    data.py
    analytics.py
    charts.py
    prediction.py
```

---

## ✅ Installation Steps
From inside `python-advanced/Aviation-Intelligence-Dashboard`:

```bash
pip install -r requirements.txt
```

---

## ▶️ How to Run the Dashboard
```bash
streamlit run app.py
```

The dashboard expects:
- `dataset/flights.csv`
- `models/delay_prediction_model.pkl` (for prediction panel)

---

## 🏋️ Model Training Explanation
Training is implemented in `prediction_model.py`.

### Key points
- Target variable: `arr_delay`
- Features: numeric delay driver counts (`arr_flights`, `carrier_ct`, `weather_ct`, `nas_ct`, `security_ct`, `late_aircraft_ct`)
- Model: `RandomForestRegressor`
- Persistence: `joblib.dump(model, "models/delay_prediction_model.pkl")`

This separation (offline training vs. online inference) mirrors production engineering patterns:
- stable artifact loading
- deterministic feature ordering
- consistent inference input coercion

---

## 💼 Business Insights (What Stakeholders Can Learn)
The dashboard is designed to support **operational decision-making**:
- 📌 Identify **airlines** that consistently accumulate delays and cancellations
- 📌 Pinpoint **airports** where operational interventions may be most impactful
- 📌 Detect **seasonality** via monthly × yearly heatmaps
- 📌 Quantify **weather-related delay influence** and validate it through correlation views
- 📌 Use prediction inputs to simulate scenarios and prioritize operational readiness

---

## 🔮 Future Improvements (Roadmap)
Aligned with `TODO.md`:
- 🧩 Refactor `app.py` into cleaner render functions + layout consistency
- 🛡️ Harden `src/data.py`, `src/analytics.py`, and `src/charts.py` for robustness
- 🗺️ Improve Folium map robustness and UX messaging when markers can’t render
- 🤖 Improve prediction system validation, loading UX, and model interface checks
- 🧪 Add smoke tests and improve documentation coverage (docstrings + architecture notes)

---

## 🚀 Deployment
### Option A: Streamlit Community Cloud
1. Push the repository to GitHub
2. Connect the repo to Streamlit Cloud
3. Ensure required files are present:
   - `dataset/flights.csv`
   - `models/delay_prediction_model.pkl`
4. Set entrypoint to `app.py`

### Option B: Containerized / Enterprise deployment (recommended)
- Build a container with the same Python dependencies from `requirements.txt`
- Mount or bake-in `dataset/` and `models/`
- Deploy behind a standard reverse proxy (Nginx/Traefik) for secure access

---

## 🌟 Recruiter-Focused Presentation
If you’re evaluating this project as a software/ML candidate, this repository demonstrates:
- ✅ **End-to-end analytics engineering** (data → features → insights → visuals)
- ✅ **Production-minded dashboard design** (filters, KPIs, defensive charting, consistent UX)
- ✅ **ML integration into a real user workflow** (saved artifact loading + predictable inference)
- ✅ **Interpretability** (feature importance visualization when available)
- ✅ **Enterprise tone documentation** (architecture + deployment readiness)

---

## 📌 Notes
- Screenshots are intentionally left as a section to populate with your exported UI images.
- The prediction panel uses the saved model artifact in `models/` and expects the dashboard feature order used by the training pipeline.

