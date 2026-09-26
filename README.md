# GreenVolt AI — EV Intelligence Platform

A full-stack, multi-module AI platform for Electric Vehicle analytics in India. GreenVolt AI combines machine learning models, real-time dashboards, and data-driven insights to analyze, predict, and monitor every major aspect of EV adoption — from charging demand and fleet health to cost savings and carbon impact.

The system is made up of four independent modules, each with its own backend API and React frontend, all launched from a single orchestration script (`Run_all.py`).

---

## Table of Contents

- [Architecture Overview](#architecture-overview)
- [Module 1 — EV Charging Demand Prediction](#module-1--ev-charging-demand-prediction)
- [Module 2 — EV Adoption Growth Dashboard](#module-2--ev-adoption-growth-dashboard)
- [Module 3 — EV Predictive Maintenance](#module-3--ev-predictive-maintenance)
- [Module 4 — EV Cost & Carbon Analysis](#module-4--ev-cost--carbon-analysis)
- [Central Hub Dashboard](#central-hub-dashboard)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Setup & Installation](#setup--installation)
- [Running the Project](#running-the-project)
- [Port Map](#port-map)
- [Dataset Sources](#dataset-sources)
- [ML Models Summary](#ml-models-summary)

---

## Architecture Overview

```
project/
├── Run_all.py                        # Launches all 9 services (4 backends + 5 frontends)
├── ev-dashboard/                     # Central hub dashboard (port 3000)
├── EV-Charging-Demand-System/        # Module 1 — Charging demand map
│   ├── backend/                      # FastAPI — port 8000
│   └── frontend/                     # React — port 3003
├── ev-adoption-growth/               # Module 2 — Adoption forecasting
│   ├── app.py                        # Flask — port 5000
│   └── frontend/                     # React — port 3002
├── ev_failure/                       # Module 3 — Predictive maintenance
│   ├── app.py                        # FastAPI — port 8003
│   └── ev-dashboard/                 # React — port 3001
└── ev_cost_carbon/                   # Module 4 — Cost & carbon comparison
    ├── main.py                       # FastAPI — port 8002
    └── frontend/                     # React — port 3004
```

All modules are independent — they can be run individually or together via `Run_all.py`.

---

## Module 1 — EV Charging Demand Prediction

**Backend:** FastAPI &nbsp;|&nbsp; **Port:** 8000 &nbsp;|&nbsp; **Frontend Port:** 3003

Predicts EV charging demand scores across Indian cities and visualizes them on an interactive Leaflet map. Users input infrastructure parameters (charger count, occupancy, EV growth rate, population density) and the API scores every city in the dataset against user input to classify demand as **Low**, **Medium**, or **High**.

### How it Works

- Uses `city_demand_index.csv` containing real city-level data (coordinates, charger counts, occupancy, growth rates)
- Computes an infrastructure gap score by comparing user demand pressure against each city's capacity
- Normalizes scores to 0–100 and classifies with dynamic thresholds (< 35 = Low, 35–70 = Medium, > 70 = High)
- Returns city name, score, demand level, and lat/lon for map rendering

### API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Health check |
| POST | `/predict` | Predict demand level for all cities given user inputs |

### Input Schema (`POST /predict`)

```json
{
  "charger_count": 10,
  "fast_ratio": 0.4,
  "avg_sessions": 50,
  "occupancy": 0.75,
  "ev_growth": 0.3,
  "population_density": 5000
}
```

### Frontend Features

- Interactive map of India (React Leaflet) with color-coded city markers
- Demand level legend (Low / Medium / High)
- City-wise score table with filtering

---

## Module 2 — EV Adoption Growth Dashboard

**Backend:** Flask &nbsp;|&nbsp; **Port:** 5000 &nbsp;|&nbsp; **Frontend Port:** 3002

Analyzes historical EV registration data from 2001 to 2024 across vehicle categories and forecasts future adoption trends using scikit-learn regression models. The dashboard provides a comprehensive view of India's EV market trajectory.

### How it Works

- Loads `ev_cat_01-24.csv` (category-wise EV registrations by date)
- Trains per-category Linear Regression models on log-transformed sales data
- Predicts future registrations for any year and category using `category_future_model1.pkl`
- Aggregates trends for CO2 impact, charging infrastructure needs, and market value estimates
- Performs KMeans clustering on Public Charging Stations (PCS) data to segment states

### API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/yearly-trend` | Total EV registrations by year (2001–2024) |
| GET | `/api/categories` | List of all vehicle categories available for prediction |
| POST | `/api/predict` | Predict registrations for a given year and category |
| POST | `/api/comprehensive-predict` | Extended prediction with CO2, PCS needs, market value, insights |
| GET | `/api/top5-growth` | Top 5 categories by predicted growth to 2035 |
| GET | `/api/co2-reduction` | Estimated CO2 reduction (tons) per category by 2035 |
| GET | `/api/2w-vs-4w` | Annual comparison of 2-wheeler vs 4-wheeler EV registrations |
| GET | `/api/forecast` | Full forecast from 2015 to 2035 using `ev_growth_model.pkl` |
| GET | `/api/pcs-ranking` | Top 15 states by current operational PCS count |
| GET | `/api/pcs-projection` | Top 10 states by projected PCS count in 5 years (20% annual growth) |
| GET | `/api/pcs-clustering` | KMeans (k=3) clustering of states by PCS count |

### Frontend Features

- Yearly trend line chart
- Category-wise forecast with year slider
- Top 5 growth leaders bar chart
- CO2 reduction card
- 2-wheeler vs 4-wheeler comparison chart
- PCS ranking, clustering, and projection cards
- Comprehensive prediction panel with auto-generated insights
- CAGR analysis chart
- Animated KPI cards (Framer Motion)

---

## Module 3 — EV Predictive Maintenance

**Backend:** FastAPI &nbsp;|&nbsp; **Port:** 8003 &nbsp;|&nbsp; **Frontend Port:** 3001

Real-time fleet health monitoring and failure prediction using a hybrid ML pipeline. Combines XGBoost for failure probability classification and a CNN-LSTM deep learning model for Remaining Useful Life (RUL) prediction. Fleet data is persisted to MongoDB Atlas.

### How it Works

- Loads `EV_Predictive_Maintenance_Dataset_15min.csv` (15-minute interval telemetry: battery temperature, motor temperature, motor vibration, SoC, SoH, brake wear, etc.)
- **XGBoost classifier** predicts failure probability (0–1) from current vehicle state
- **CNN-LSTM model** (Conv1D → LSTM → FC) predicts RUL from a 10-step telemetry sequence
- **SHAP TreeExplainer** identifies the top features driving each failure prediction
- Fleet samples are written to MongoDB Atlas on every `/fleet` call for persistence and history

### ML Models

| Model | Task | Architecture |
|-------|------|--------------|
| `xgb_classifier.pkl` | Failure probability | XGBoost classifier |
| `cnn_lstm_model.pth` | Remaining Useful Life | Conv1D(5→32, k=3) → LSTM(32→64) → FC(64→1) |
| `scaler.pkl` | XGBoost feature scaling | StandardScaler |
| `lstm_X_scaler.pkl` / `lstm_y_scaler.pkl` | LSTM input/output scaling | StandardScaler |

### API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Health check |
| GET | `/fleet` | Sample 5 vehicles, predict failure probability, save to MongoDB |
| GET | `/fleet-history` | Retrieve all saved fleet records from MongoDB |
| GET | `/top-vehicle` | Vehicle with highest failure probability from current sample |
| GET | `/fleet-health` | Overall fleet health score (0–100) based on historical records |
| GET | `/vehicle-history` | All vehicle records from MongoDB |
| GET | `/shap-analysis` | SHAP feature importance for a random vehicle |
| GET | `/vehicle-analysis` | Full analysis: failure %, RUL, component risk, charging advice, cost, trends |

### Vehicle Analysis Output

```json
{
  "failure_percent": 72,
  "rul_days": 14.3,
  "component_risk": { "battery": "High", "motor": "Low", "brake": "Low" },
  "charging_advice": "Charge Immediately",
  "cost_now": 14400,
  "cost_delayed": 21600,
  "overall_health": 68,
  "range_km": 57,
  "trend_summary": { "Battery_Temperature": 3.2, "SoH": -0.04 }
}
```

### Frontend Features

- Live fleet health gauge
- Vehicle failure probability cards (color-coded by risk level)
- RUL timeline chart
- Component risk badges (battery, motor, brakes)
- SHAP feature importance bar chart
- Charging advice alert
- Fleet history table from MongoDB
- Maintenance cost comparison (act now vs delay)

---

## Module 4 — EV Cost & Carbon Analysis

**Backend:** FastAPI (GreenVolt EV Cost & Carbon API) &nbsp;|&nbsp; **Port:** 8002 &nbsp;|&nbsp; **Frontend Port:** 3004

Compares the total cost of ownership between EVs and fossil fuel vehicles. Predicts annual cost savings, carbon footprint reduction, payback period, eco score, and environmental benefit score using two model tiers — a lightweight basic model and a research-grade model with 70+ engineered features.

### How it Works

- **Basic model:** Uses core financial and usage inputs (fuel price, electricity price, daily distance, mileage, maintenance costs, subsidies) to predict `cost_savings_rs_per_year` and `carbon_reduction_kg_per_year`
- **Research model:** Extends with 70+ features including battery stress, charging behavior, driver style, regional data, fleet metrics, temporal features, and financial indices
- Both models use **RandomForestRegressor** trained on `greenvolt_ev_dataset_*.csv`
- **SHAP TreeExplainer** returns the top 5 features influencing each prediction
- Generates bar chart images saved to `/static/` and served via the API

### API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Health check |
| POST | `/predict/basic` | Basic 2-model prediction (cost + carbon savings) |
| POST | `/predict/research` | Research-grade prediction with 70+ features |
| GET | `/model-info` | Model metadata and feature list |

### Prediction Output (both tiers)

```json
{
  "cost_savings_rs_per_year": 48500,
  "carbon_reduction_kg_per_year": 1820,
  "payback_period_years": 4.2,
  "eco_score": 76.3,
  "monthly_savings_rs": 4041,
  "trees_saved_equivalent": 86,
  "cost_savings_5yr_rs": 242500,
  "carbon_reduction_5yr_kg": 9100,
  "shap_top5": [
    { "feature": "fuel_cost_rs_per_year", "impact": 0.432 },
    { "feature": "annual_distance_km", "impact": 0.218 }
  ],
  "chart_url": "/static/chart_abc123.png"
}
```

### Frontend Features

- 5-step wizard form for inputting vehicle and usage parameters
- Side-by-side cost comparison cards (EV vs fuel)
- Payback period timeline visualization
- CO2 savings and eco score gauge
- SHAP top-5 feature importance chart
- Trees saved equivalent display
- Basic vs Research model toggle

---

## Central Hub Dashboard

**Port:** 3000 &nbsp;|&nbsp; **Folder:** `ev-dashboard/`

A unified command center that links to all four module dashboards. Shows live KPI summary cards (battery health pulled from the maintenance API), a demand chart, and navigation tiles for each module.

### Navigation Tiles

| Tile | Target | Description |
|------|--------|-------------|
| Failure Dashboard | `localhost:3001` | Fleet faults and anomaly traces |
| EV Demand | `localhost:3003` | Charging demand heatmap |
| EV Adoption | `localhost:3002` | Market growth and forecasting |
| EV Cost-Carbon | `localhost:3004` | Cost and sustainability comparison |

---

## Tech Stack

| Category | Technology |
|----------|------------|
| Backend frameworks | FastAPI, Flask |
| ML / AI | scikit-learn, XGBoost, PyTorch (CNN-LSTM), SHAP |
| Data processing | Pandas, NumPy, Matplotlib |
| Frontend | React 18/19, Recharts, Chart.js, React-Leaflet, Framer Motion, Axios |
| Database | MongoDB Atlas (via PyMongo) |
| Orchestration | Python subprocess launcher (`Run_all.py`) |
| API server | Uvicorn (FastAPI), Flask dev server |

---

## Project Structure

```
project/
│
├── Run_all.py                            # Master launcher for all services
│
├── ev-dashboard/                         # Central hub (port 3000)
│   └── src/
│       └── components/
│           └── Dashboard.js              # Main hub UI with KPI cards and nav tiles
│
├── EV-Charging-Demand-System/            # Module 1
│   ├── backend/
│   │   ├── main.py                       # FastAPI app — port 8000
│   │   └── city_demand_index.csv         # City-level infrastructure data
│   └── frontend/                         # React app — port 3003
│       └── src/
│
├── ev-adoption-growth/                   # Module 2
│   ├── app.py                            # Flask app — port 5000
│   ├── data/                             # ev_cat_01-24.csv, OperationalPC.csv, etc.
│   ├── models/                           # category_future_model1.pkl, ev_growth_model.pkl, etc.
│   └── frontend/                         # React app — port 3002
│       └── src/
│           └── components/              # 20+ chart and card components
│
├── ev_failure/                           # Module 3
│   ├── app.py                            # FastAPI app — port 8003
│   ├── data/
│   │   └── EV_Predictive_Maintenance_Dataset_15min.csv
│   ├── xgb_classifier.pkl
│   ├── cnn_lstm_model.pth
│   ├── scaler.pkl
│   ├── lstm_X_scaler.pkl
│   └── lstm_y_scaler.pkl
│
└── ev_cost_carbon/                       # Module 4
    ├── main.py                           # FastAPI app — port 8002
    ├── model/
    │   ├── cost_model_basic.pkl
    │   ├── carbon_model_basic.pkl
    │   ├── cost_model_research.pkl
    │   ├── carbon_model_research.pkl
    │   ├── basic_encoders.pkl / basic_features.pkl
    │   └── research_encoders.pkl / research_features.pkl
    └── frontend/                         # React app — port 3004
        └── src/
```

---

## Prerequisites

- Python 3.9+
- Node.js 18+ and npm
- MongoDB Atlas account (for Module 3 fleet persistence)
- Git

---

## Setup & Installation

### 1. Clone the Repository

```bash
git clone https://github.com/<your-username>/greenvolt-ev-platform.git
cd greenvolt-ev-platform
```

### 2. Create a Python Virtual Environment

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate
```

### 3. Install Python Dependencies

Install all required Python packages for every module:

```bash
pip install fastapi uvicorn flask flask-cors pandas numpy scikit-learn xgboost shap joblib torch pymongo matplotlib
```

Or install module-by-module:

```bash
# Module 2 — Adoption
pip install -r ev-adoption-growth/requirements.txt

# Module 3 — Failure
pip install -r ev_failure/requirements.txt
```

### 4. Install Frontend Dependencies

Run `npm install` inside each frontend folder:

```bash
cd ev-dashboard && npm install && cd ..
cd EV-Charging-Demand-System/frontend && npm install && cd ../..
cd ev-adoption-growth/frontend && npm install && cd ../..
cd ev_cost_carbon/frontend && npm install && cd ../..
```

For Module 3 frontend (if separate from hub dashboard):

```bash
cd ev_failure/ev-dashboard && npm install && cd ../..
```

### 5. Configure MongoDB (Module 3)

The predictive maintenance backend connects to MongoDB Atlas. Update the connection string in `ev_failure/app.py` if needed:

```python
client = MongoClient("mongodb+srv://<user>:<password>@<cluster>.mongodb.net/")
```

---

## Running the Project

### Option A — Run Everything at Once

```bash
python Run_all.py
```

This launches all 9 services simultaneously (4 Python backends + 5 React frontends). Press `Ctrl+C` to stop all.

### Option B — Run Modules Individually

**Module 1 — Charging Demand:**

```bash
# Backend
cd EV-Charging-Demand-System/backend
uvicorn main:app --port 8000 --reload

# Frontend (separate terminal)
cd EV-Charging-Demand-System/frontend
npm start  # runs on port 3003
```

**Module 2 — Adoption Growth:**

```bash
# Backend
cd ev-adoption-growth
python app.py  # runs on port 5000

# Frontend (separate terminal)
cd ev-adoption-growth/frontend
npm start  # runs on port 3002
```

**Module 3 — Predictive Maintenance:**

```bash
# Backend
uvicorn ev_failure.app:app --port 8003 --reload

# Frontend (separate terminal)
cd ev_failure/ev-dashboard
npm start  # runs on port 3001
```

**Module 4 — Cost & Carbon:**

```bash
# Backend
uvicorn ev_cost_carbon.main:app --port 8002 --reload

# Frontend (separate terminal)
cd ev_cost_carbon/frontend
npm start  # runs on port 3004
```

**Central Hub Dashboard:**

```bash
cd ev-dashboard
npm start  # runs on port 3000
```

---

## Port Map

| Service | URL |
|---------|-----|
| Central Hub Dashboard | http://localhost:3000 |
| Predictive Maintenance Frontend | http://localhost:3001 |
| EV Adoption Growth Frontend | http://localhost:3002 |
| EV Charging Demand Frontend | http://localhost:3003 |
| EV Cost & Carbon Frontend | http://localhost:3004 |
| Charging Demand API | http://localhost:8000 |
| Cost & Carbon API | http://localhost:8002 |
| Predictive Maintenance API | http://localhost:8003 |
| Adoption Growth API | http://localhost:5000 |

---

## Dataset Sources

| Dataset | Used In | Description |
|---------|---------|-------------|
| `city_demand_index.csv` | Module 1 | City-level EV infrastructure data (charger count, occupancy, growth rate, coordinates) |
| `ev_cat_01-24.csv` | Module 2 | Monthly EV registrations by category (2001–2024) |
| `OperationalPC.csv` | Module 2 | State-wise operational public charging stations |
| `ev_sales_by_makers_and_cat_15-24.csv` | Module 2 | EV sales by manufacturer and category (2015–2024) |
| `EV Maker by Place.csv` | Module 2 | EV manufacturer locations |
| `EV_Predictive_Maintenance_Dataset_15min.csv` | Module 3 | 15-minute interval EV telemetry (temperature, SoC, SoH, vibration, brake wear) |
| `greenvolt_ev_dataset_*.csv` | Module 4 | EV vs fuel vehicle cost and carbon comparison records |

---

## ML Models Summary

| Module | Model | Algorithm | Task |
|--------|-------|-----------|------|
| 1 — Charging Demand | Scoring algorithm | Rule-based + normalization | City demand classification (Low/Medium/High) |
| 2 — Adoption Growth | `ev_growth_model.pkl` | Linear Regression (log-transform) | Total EV registrations forecast (2015–2035) |
| 2 — Adoption Growth | `category_future_model1.pkl` | Per-category Linear Regression | Category-wise EV registrations forecast |
| 2 — Adoption Growth | `pcs_infra_classifier.pkl` | Classifier | PCS infrastructure classification |
| 2 — Adoption Growth | `pcs_state_growth_model.pkl` | Regressor | State-level PCS growth prediction |
| 3 — Maintenance | `xgb_classifier.pkl` | XGBoost | Failure probability (0–1) |
| 3 — Maintenance | `cnn_lstm_model.pth` | CNN-LSTM (PyTorch) | Remaining Useful Life (days) |
| 4 — Cost & Carbon | `cost_model_basic.pkl` | Random Forest Regressor | Annual cost savings (basic features) |
| 4 — Cost & Carbon | `carbon_model_basic.pkl` | Random Forest Regressor | Annual carbon reduction (basic features) |
| 4 — Cost & Carbon | `cost_model_research.pkl` | Random Forest Regressor | Annual cost savings (70+ features) |
| 4 — Cost & Carbon | `carbon_model_research.pkl` | Random Forest Regressor | Annual carbon reduction (70+ features) |

---

## Notes

- ML model `.pkl` and `.pth` files are excluded from version control (see `.gitignore`). Train them locally using the provided training scripts in each module's `models/` or `ml/` folder before running the backends.
- Large CSV datasets are also excluded. Place them in their respective `data/` directories before starting the backends.
- The MongoDB connection string in `ev_failure/app.py` contains credentials — replace it with an environment variable before pushing to a public repository.
