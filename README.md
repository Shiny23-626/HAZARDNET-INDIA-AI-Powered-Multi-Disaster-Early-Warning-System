# 🌊 HazardNet India — AI-Powered Multi-Disaster Early Warning System

> **ITERYX '26 Hackathon Submission** | Problem Statement #08 | Domain: AI & Machine Learning  
> Team: **THE Executioners** | Leader: Amsapriya K | College: Agni College of Technology

---

## 📌 Overview

**HazardNet India** is a hyperlocal, AI-driven disaster forecasting and early warning system built to predict four major natural disasters — **Flood, Cyclone, Landslide, and Heatwave** — across India in real time.

Unlike existing systems that issue broad district-level alerts, HazardNet India focuses on:
- **Street-level risk prediction** using ML ensembles
- **Multilingual alerts** in 16 Indian regional languages
- **Actionable evacuation guidance** for citizens, farmers, and government agencies
- **Admin SOS dashboard** for emergency response coordination

---

## 🚨 Problem Statement

| Pain Point | Impact |
|---|---|
| Delayed disaster alerts | Increased casualties and economic loss |
| No region-specific prediction | Inaccurate risk levels for local communities |
| Language barriers | Rural populations miss critical warnings |
| Single-disaster systems | Miss compound/sequential disaster events |

---

## ✅ Solution Highlights

- 🤖 **Multi-hazard ML model** (Random Forest / Gradient Boosting) trained on IMD + Kaggle datasets
- 🗺️ **Interactive geospatial heatmaps** for flood, cyclone, landslide, and heatwave risk zones
- 📡 **Live weather integration** via OpenWeatherMap API
- 🌐 **16 languages** — English, Hindi, Tamil, Telugu, Malayalam, Kannada, Bengali, Odia, Marathi, Gujarati, Punjabi, Assamese, Urdu, Nepali, Konkani + more
- 🚨 **SOS Admin Dashboard** with resource management and rescue team coordination
- 📊 **EDA & model performance** dashboards built-in

---

## 🏗️ Technical Architecture

```
User Input (Location + Environmental Params)
        │
        ▼
┌─────────────────────────────┐
│     Streamlit Frontend      │  ← This app
│  (Dashboard + Predictor)    │
└────────────┬────────────────┘
             │
    ┌────────▼────────┐
    │   FastAPI Back  │  (future)
    │  end + ML Model │
    └────────┬────────┘
             │
    ┌────────▼────────────────────────┐
    │         ML Pipeline             │
    │  Random Forest / XGBoost /      │
    │  LSTM + Attention / TFT         │
    │  MultiOutputClassifier          │
    └────────┬────────────────────────┘
             │
    ┌────────▼────────────────────────┐
    │        Data Sources             │
    │  IMD · Kaggle · NASA POWER      │
    │  OpenWeatherMap · NDMA          │
    └─────────────────────────────────┘
```

---

## 📁 Project Structure

```
HazardNet_India/
│
├── app.py                              # Main Streamlit application
├── api_utils.py                        # OpenWeatherMap API helpers
├── model_multihazard.pkl               # Pre-trained Random Forest model
├── requirements.txt                    # Python dependencies
├── .gitignore
│
└── data/
    └── flood_dataset_corrected_multihazard.csv   # Training dataset
```

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/<your-username>/HazardNet_India.git
cd HazardNet_India
```

### 2. Create and activate a virtual environment (recommended)

```bash
python -m venv venv
source venv/bin/activate        # Linux/macOS
venv\Scripts\activate           # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Streamlit app

```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`.

---

## ⚙️ Configuration

### Dataset
On launch, the app looks for the dataset at:
```
data/flood_dataset_corrected_multihazard.csv
```
You can also upload a CSV directly through the sidebar uploader in the app.

### OpenWeatherMap API Key (optional)
To enable **live weather data** in the "Live API Detection" tab:
1. Get a free API key from [openweathermap.org/api](https://openweathermap.org/api)
2. Enter it directly in the app's "Live API Detection" tab (not stored on disk)

To hard-code it for development, edit `api_utils.py`:
```python
API_KEY = "your_key_here"
```

> ⚠️ **Never commit your API key to GitHub.** Use `.streamlit/secrets.toml` or environment variables for production.

---

## 🧠 ML Model Details

| Feature | Details |
|---|---|
| Algorithm | Random Forest Classifier (150 trees) / Gradient Boosting |
| Task | Multi-output classification (4 binary hazard labels) + single-label overall risk |
| Features | Rainfall, Temperature, Humidity, River Discharge, Water Level, Elevation, Population Density, Land Cover, Soil Type, Season flags, Historical Floods |
| Labels | `flood_label`, `cyclone_label`, `landslide_label`, `heatwave_label`, `max_risk_label` |
| Preprocessing | StandardScaler + LabelEncoder |
| Evaluation | Accuracy, Confusion Matrix, Classification Report (per hazard) |

---

## 📊 App Tabs

| Tab | Description |
|---|---|
| 🗺️ Risk Map | Geospatial heatmap — scatter and density views per hazard |
| 📊 EDA & Insights | Distributions, year-wise trends, seasonal patterns, correlations |
| 🤖 ML Prediction | Train model, view feature importance and confusion matrix |
| 🔮 Predict My Risk | Enter custom parameters and get instant risk prediction |
| 🌤️ Live API Detection | Fetch live weather and run real-time ML prediction |
| 🚨 SOS Admin Dashboard | Emergency command centre with resource management |
| 🌐 Languages | Preview alerts in 16 Indian languages |
| 📋 Dataset | Filter and download dataset |
| ℹ️ About | Technical stack and project details |

---

## 🌍 Disasters Covered

| Disaster | High-Risk Regions |
|---|---|
| 🌊 Flood | Chennai, Kochi, Mumbai, Kolkata, Guwahati, Hyderabad |
| 🌀 Cyclone | Bhubaneswar, Kolkata, Chennai |
| ⛰️ Landslide | Kochi, Guwahati |
| 🌡️ Heatwave | Jaipur, Hyderabad, Delhi |

---

## 📡 Data Sources

- [India Meteorological Department (IMD)](https://imdpune.gov.in) — Historical rainfall & cyclone data
- [NDMA](https://ndma.gov.in) — Disaster event records
- [Kaggle — India Flood Inventory](https://kaggle.com/datasets/india-flood-inventory) — 500+ flood events
- [NASA FIRMS + IBTrACS](https://firms.modaps.eosdis.nasa.gov) — Satellite flood/fire & cyclone track data
- [OpenWeatherMap API](https://openweathermap.org/api) — Real-time weather

---

## 🗺️ Roadmap

- [x] **Phase 1 (Now):** Streamlit prototype, 20 states, 4 disaster types
- [ ] **Phase 2 (3 months):** Real-time IMD API integration + all 28 states + SMS alerts via Twilio
- [ ] **Phase 3 (6 months):** LSTM Deep Learning, Flutter mobile app, district-level alerts, SHAP explainability

---

## 🛠️ Full Tech Stack (Planned)

| Layer | Technologies |
|---|---|
| Frontend (Web) | Streamlit |
| Frontend (Mobile) | Flutter · Dart |
| Backend | FastAPI · Python |
| ML (Baseline) | Scikit-learn · XGBoost · Pandas |
| ML (Advanced) | PyTorch LSTM · TFT · Kriging · SHAP |
| Alerts | Twilio SMS · Firebase Push |
| Deployment | Render · AWS EC2 |
| Database | PostgreSQL / Firebase |

---

## 👥 Team

| Name | Role |
|---|---|
| Amsapriya K (Team Leader) | ML Model, Backend |
| Team Members | Frontend, Data, Presentation |

**College:** Agni College of Technology  
---

## 📄 License

This project is submitted as part of ITERYX '26 Hackathon. All rights reserved by THE Executioners team.

---

<p align="center">
  <b>HazardNet India — Closing the warning gap to save lives with localised, real-time ML alerts.</b><br>
  🛡️ Protecting 1.5 Billion People across 20 States and 4 Disaster Types
</p>
