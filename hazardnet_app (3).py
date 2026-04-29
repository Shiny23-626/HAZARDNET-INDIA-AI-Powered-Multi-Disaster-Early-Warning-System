"""
HazardNet India - Hyperlocal Multi-Disaster Prediction & Early Warning System
Full Streamlit Dashboard
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.multioutput import MultiOutputClassifier
import requests
import datetime
import warnings
warnings.filterwarnings("ignore")

# ─────────────────────────────────────────────────────────────────────────────
# Page Config
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="HazardNet India",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────────────────────
# Custom CSS
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .main-title {
        font-size: 2.8rem;
        font-weight: 800;
        background: linear-gradient(135deg, #1e3a5f, #e74c3c);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0.2rem;
    }
    .subtitle {
        text-align: center;
        color: #888;
        font-size: 1.1rem;
        margin-bottom: 1.5rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #1e3a5f, #2d6a9f);
        border-radius: 12px;
        padding: 1.2rem;
        color: white;
        text-align: center;
        margin-bottom: 1rem;
    }
    .metric-value {
        font-size: 2.2rem;
        font-weight: 800;
    }
    .metric-label {
        font-size: 0.85rem;
        opacity: 0.85;
        margin-top: 0.2rem;
    }
    .risk-high   { background: #e74c3c !important; }
    .risk-medium { background: #f39c12 !important; }
    .risk-low    { background: #27ae60 !important; }
    .section-header {
        font-size: 1.4rem;
        font-weight: 700;
        color: #1e3a5f;
        border-left: 4px solid #e74c3c;
        padding-left: 0.8rem;
        margin: 1.2rem 0 0.8rem;
    }
    .alert-box {
        border-radius: 10px;
        padding: 1rem 1.2rem;
        margin-bottom: 0.8rem;
        font-weight: 600;
    }
    .alert-flood    { background: #d6eaf8; border-left: 5px solid #2980b9; color: #1a5276; }
    .alert-cyclone  { background: #fdebd0; border-left: 5px solid #e67e22; color: #784212; }
    .alert-landslide{ background: #d5f5e3; border-left: 5px solid #27ae60; color: #1e8449; }
    .alert-heatwave { background: #fdedec; border-left: 5px solid #e74c3c; color: #922b21; }
    .stTabs [data-baseweb="tab"] { font-size: 1rem; font-weight: 600; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# Header
# ─────────────────────────────────────────────────────────────────────────────
st.markdown('<div class="main-title">🌊 HazardNet India</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Hyperlocal Multi-Disaster Prediction & Multilingual Early Warning System</div>', unsafe_allow_html=True)
st.markdown("---")

# ─────────────────────────────────────────────────────────────────────────────
# Sidebar
# ─────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/storm.png", width=80)
    st.title("⚙️ Settings")

    uploaded_file = st.file_uploader(
        "📂 Upload Dataset (CSV)",
        type=["csv"],
        help="Upload the HazardNet multi-hazard CSV dataset",
    )

    st.markdown("---")
    st.markdown("### 🗺️ City Filter")
    city_coords = {
        "All India": None,
        "Chennai": (13.08, 80.27),
        "Kochi": (9.93, 76.26),
        "Mumbai": (19.08, 72.88),
        "Kolkata": (22.57, 88.36),
        "Guwahati": (26.14, 91.74),
        "Jaipur": (26.91, 75.79),
        "Hyderabad": (17.38, 78.49),
        "Bhubaneswar": (20.30, 85.82),
    }
    selected_city = st.selectbox("Select City / Region", list(city_coords.keys()))

    st.markdown("---")
    st.markdown("### 📅 Year Range")
    year_range = st.slider("Select Year Range", 2015, 2025, (2015, 2025))

    st.markdown("---")
    st.markdown("### 🤖 ML Model")
    model_choice = st.selectbox(
        "Select Classifier",
        ["Random Forest", "Gradient Boosting"],
    )
    n_estimators = st.slider("Number of Estimators", 50, 300, 100, step=50)

    st.markdown("---")
    st.caption("HazardNet India v1.0 | Hackathon Submission")

# ─────────────────────────────────────────────────────────────────────────────
# Data Loading
# ─────────────────────────────────────────────────────────────────────────────
@st.cache_data
def load_data(file):
    if file is not None:
        df = pd.read_csv(file)
    else:
        # Try default path (when running with dataset in same folder)
        try:
            df = pd.read_csv("flood_dataset_corrected_multihazard__2_.csv")
        except FileNotFoundError:
            st.error("⚠️ Please upload the dataset using the sidebar uploader.")
            st.stop()
    return df

@st.cache_data
def preprocess(df):
    le_land  = LabelEncoder()
    le_soil  = LabelEncoder()
    le_risk  = LabelEncoder()
    df = df.copy()
    df["land_cover_enc"] = le_land.fit_transform(df["Land Cover"])
    df["soil_type_enc"]  = le_soil.fit_transform(df["Soil Type"])
    df["risk_label_enc"] = le_risk.fit_transform(df["max_risk_label"])
    return df, le_land, le_soil, le_risk

df_raw = load_data(uploaded_file)
df, le_land, le_soil, le_risk = preprocess(df_raw)

# Filter by year
df = df[(df["year"] >= year_range[0]) & (df["year"] <= year_range[1])]

# Filter by city (±1.5° lat/lon box)
if selected_city != "All India":
    clat, clon = city_coords[selected_city]
    df = df[
        (df["Latitude"].between(clat - 1.5, clat + 1.5)) &
        (df["Longitude"].between(clon - 1.5, clon + 1.5))
    ]
    if df.empty:
        st.warning(f"No data found near {selected_city}. Showing all-India data.")
        df, le_land, le_soil, le_risk = preprocess(df_raw)
        df = df[(df["year"] >= year_range[0]) & (df["year"] <= year_range[1])]

# ─────────────────────────────────────────────────────────────────────────────
# Top KPI Cards
# ─────────────────────────────────────────────────────────────────────────────
total     = len(df)
n_flood   = df["flood_label"].sum()
n_cyclone = df["cyclone_label"].sum()
n_land    = df["landslide_label"].sum()
n_heat    = df["heatwave_label"].sum()

c1, c2, c3, c4, c5 = st.columns(5)
for col, label, val, cls in [
    (c1, "📊 Total Records",   total,     ""),
    (c2, "🌊 Flood Events",    n_flood,   "risk-high"),
    (c3, "🌀 Cyclone Events",  n_cyclone, "risk-medium"),
    (c4, "⛰️ Landslide Events", n_land,   "risk-medium"),
    (c5, "🌡️ Heatwave Events", n_heat,   "risk-high"),
]:
    col.markdown(
        f'<div class="metric-card {cls}"><div class="metric-value">{val:,}</div>'
        f'<div class="metric-label">{label}</div></div>',
        unsafe_allow_html=True,
    )

# ─────────────────────────────────────────────────────────────────────────────
# Tabs
# ─────────────────────────────────────────────────────────────────────────────
tabs = st.tabs([
    "🗺️ Risk Map",
    "📊 EDA & Insights",
    "🤖 ML Prediction",
    "🔮 Predict My Risk",
    "🌤️ Live API Detection",
    "🚨 SOS Admin Dashboard",
    "🌐 Languages",
    "📋 Dataset",
    "ℹ️ About",
])

# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 — RISK MAP
# ══════════════════════════════════════════════════════════════════════════════
with tabs[0]:
    st.markdown('<div class="section-header">🗺️ Geospatial Risk Heatmap</div>', unsafe_allow_html=True)

    hazard_sel = st.selectbox(
        "Select Hazard to Visualize",
        ["max_risk_label", "flood_label", "cyclone_label", "landslide_label", "heatwave_label"],
        format_func=lambda x: {
            "max_risk_label": "🔴 Overall Max Risk",
            "flood_label":    "🌊 Flood Risk",
            "cyclone_label":  "🌀 Cyclone Risk",
            "landslide_label":"⛰️ Landslide Risk",
            "heatwave_label": "🌡️ Heatwave Risk",
        }[x],
    )

    sample = df.sample(min(2000, len(df)), random_state=42)

    color_map = {
        "flood":        "#2980b9",
        "cyclone":      "#e67e22",
        "landslide":    "#27ae60",
        "heatwave":     "#e74c3c",
        "no_major_risk":"#95a5a6",
    }

    if hazard_sel == "max_risk_label":
        fig_map = px.scatter_mapbox(
            sample,
            lat="Latitude", lon="Longitude",
            color="max_risk_label",
            color_discrete_map=color_map,
            size_max=10, zoom=4,
            mapbox_style="carto-positron",
            title="Multi-Hazard Risk Distribution Across India",
            hover_data=["Rainfall (mm)", "Temperature (°C)", "Water Level (m)"],
        )
    else:
        fig_map = px.density_mapbox(
            sample[sample[hazard_sel] == 1],
            lat="Latitude", lon="Longitude",
            radius=12, zoom=4,
            mapbox_style="carto-positron",
            title=f"{hazard_sel.replace('_label','').title()} Risk Density Map",
            color_continuous_scale="Reds",
        )

    fig_map.update_layout(height=520, margin=dict(l=0, r=0, t=40, b=0))
    st.plotly_chart(fig_map, use_container_width=True)

    st.markdown('<div class="section-header">📍 Risk Legend</div>', unsafe_allow_html=True)
    lc1, lc2, lc3, lc4, lc5 = st.columns(5)
    for col, emoji, label, color in [
        (lc1, "🌊", "Flood",        "#2980b9"),
        (lc2, "🌀", "Cyclone",      "#e67e22"),
        (lc3, "⛰️", "Landslide",    "#27ae60"),
        (lc4, "🌡️", "Heatwave",    "#e74c3c"),
        (lc5, "✅", "No Major Risk","#95a5a6"),
    ]:
        col.markdown(
            f'<div style="background:{color};border-radius:8px;padding:0.6rem;'
            f'text-align:center;color:white;font-weight:700">{emoji} {label}</div>',
            unsafe_allow_html=True,
        )

# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 — EDA & INSIGHTS
# ══════════════════════════════════════════════════════════════════════════════
with tabs[1]:
    st.markdown('<div class="section-header">📊 Exploratory Data Analysis</div>', unsafe_allow_html=True)

    # --- Row 1: Distribution + Pie
    r1c1, r1c2 = st.columns(2)

    with r1c1:
        risk_counts = df["max_risk_label"].value_counts().reset_index()
        risk_counts.columns = ["Risk Type", "Count"]
        fig_bar = px.bar(
            risk_counts, x="Risk Type", y="Count",
            color="Risk Type",
            color_discrete_map=color_map,
            title="Risk Type Distribution",
            text="Count",
        )
        fig_bar.update_traces(textposition="outside")
        fig_bar.update_layout(showlegend=False, height=380)
        st.plotly_chart(fig_bar, use_container_width=True)

    with r1c2:
        fig_pie = px.pie(
            risk_counts, names="Risk Type", values="Count",
            color="Risk Type",
            color_discrete_map=color_map,
            title="Risk Type Proportion",
            hole=0.4,
        )
        fig_pie.update_layout(height=380)
        st.plotly_chart(fig_pie, use_container_width=True)

    # --- Row 2: Yearly trend
    st.markdown('<div class="section-header">📅 Year-wise Disaster Trends</div>', unsafe_allow_html=True)
    yearly = df.groupby("year")[["flood_label", "cyclone_label", "landslide_label", "heatwave_label"]].sum().reset_index()
    yearly.columns = ["Year", "Flood", "Cyclone", "Landslide", "Heatwave"]
    fig_trend = px.line(
        yearly, x="Year",
        y=["Flood", "Cyclone", "Landslide", "Heatwave"],
        markers=True,
        title="Disaster Events per Year",
        color_discrete_map={"Flood":"#2980b9","Cyclone":"#e67e22","Landslide":"#27ae60","Heatwave":"#e74c3c"},
    )
    fig_trend.update_layout(height=380, legend_title="Hazard Type")
    st.plotly_chart(fig_trend, use_container_width=True)

    # --- Row 3: Environmental correlations
    st.markdown('<div class="section-header">🔗 Environmental Feature Analysis</div>', unsafe_allow_html=True)
    r3c1, r3c2 = st.columns(2)

    with r3c1:
        fig_box = px.box(
            df, x="max_risk_label", y="Rainfall (mm)",
            color="max_risk_label",
            color_discrete_map=color_map,
            title="Rainfall Distribution by Risk Type",
        )
        fig_box.update_layout(showlegend=False, height=380)
        st.plotly_chart(fig_box, use_container_width=True)

    with r3c2:
        fig_box2 = px.box(
            df, x="max_risk_label", y="Temperature (°C)",
            color="max_risk_label",
            color_discrete_map=color_map,
            title="Temperature Distribution by Risk Type",
        )
        fig_box2.update_layout(showlegend=False, height=380)
        st.plotly_chart(fig_box2, use_container_width=True)

    # --- Row 4: Scatter
    r4c1, r4c2 = st.columns(2)
    with r4c1:
        fig_sc = px.scatter(
            df.sample(min(1000, len(df)), random_state=42),
            x="Rainfall (mm)", y="Water Level (m)",
            color="max_risk_label",
            color_discrete_map=color_map,
            title="Rainfall vs Water Level",
            opacity=0.6,
        )
        fig_sc.update_layout(height=380)
        st.plotly_chart(fig_sc, use_container_width=True)

    with r4c2:
        fig_sc2 = px.scatter(
            df.sample(min(1000, len(df)), random_state=42),
            x="Elevation (m)", y="River Discharge (m³/s)",
            color="max_risk_label",
            color_discrete_map=color_map,
            title="Elevation vs River Discharge",
            opacity=0.6,
        )
        fig_sc2.update_layout(height=380)
        st.plotly_chart(fig_sc2, use_container_width=True)

    # --- Correlation heatmap
    st.markdown('<div class="section-header">🔢 Feature Correlation Matrix</div>', unsafe_allow_html=True)
    num_cols = [
        "Rainfall (mm)", "Temperature (°C)", "Humidity (%)",
        "River Discharge (m³/s)", "Water Level (m)", "Elevation (m)",
        "Population Density", "flood_label", "cyclone_label",
        "landslide_label", "heatwave_label",
    ]
    corr = df[num_cols].corr()
    fig_corr = px.imshow(
        corr, text_auto=".2f", aspect="auto",
        color_continuous_scale="RdBu_r",
        title="Feature Correlation Heatmap",
        zmin=-1, zmax=1,
    )
    fig_corr.update_layout(height=500)
    st.plotly_chart(fig_corr, use_container_width=True)

    # --- Season Analysis
    st.markdown('<div class="section-header">🌤️ Seasonal Disaster Patterns</div>', unsafe_allow_html=True)
    season_df = pd.DataFrame({
        "Season": ["Monsoon", "Summer", "Cyclone Season"],
        "Flood":     [df[df["is_monsoon"]==1]["flood_label"].sum(),
                      df[df["is_summer"]==1]["flood_label"].sum(),
                      df[df["is_cyclone_season"]==1]["flood_label"].sum()],
        "Cyclone":   [df[df["is_monsoon"]==1]["cyclone_label"].sum(),
                      df[df["is_summer"]==1]["cyclone_label"].sum(),
                      df[df["is_cyclone_season"]==1]["cyclone_label"].sum()],
        "Heatwave":  [df[df["is_monsoon"]==1]["heatwave_label"].sum(),
                      df[df["is_summer"]==1]["heatwave_label"].sum(),
                      df[df["is_cyclone_season"]==1]["heatwave_label"].sum()],
    })
    fig_season = px.bar(
        season_df.melt(id_vars="Season", var_name="Hazard", value_name="Events"),
        x="Season", y="Events", color="Hazard", barmode="group",
        color_discrete_map={"Flood":"#2980b9","Cyclone":"#e67e22","Heatwave":"#e74c3c"},
        title="Disaster Events by Season",
    )
    fig_season.update_layout(height=380)
    st.plotly_chart(fig_season, use_container_width=True)

    # --- Land Cover & Soil
    r5c1, r5c2 = st.columns(2)
    with r5c1:
        lc_counts = df["Land Cover"].value_counts().reset_index()
        lc_counts.columns = ["Land Cover", "Count"]
        fig_lc = px.bar(lc_counts, x="Land Cover", y="Count",
                        color="Land Cover", title="Records by Land Cover",
                        text="Count")
        fig_lc.update_traces(textposition="outside")
        fig_lc.update_layout(showlegend=False, height=350)
        st.plotly_chart(fig_lc, use_container_width=True)

    with r5c2:
        soil_counts = df["Soil Type"].value_counts().reset_index()
        soil_counts.columns = ["Soil Type", "Count"]
        fig_soil = px.bar(soil_counts, x="Soil Type", y="Count",
                          color="Soil Type", title="Records by Soil Type",
                          text="Count")
        fig_soil.update_traces(textposition="outside")
        fig_soil.update_layout(showlegend=False, height=350)
        st.plotly_chart(fig_soil, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 3 — ML PREDICTION
# ══════════════════════════════════════════════════════════════════════════════
with tabs[2]:
    st.markdown('<div class="section-header">🤖 Machine Learning Model Training</div>', unsafe_allow_html=True)

    FEATURES = [
        "Rainfall (mm)", "Temperature (°C)", "Humidity (%)",
        "River Discharge (m³/s)", "Water Level (m)", "Elevation (m)",
        "Population Density", "Infrastructure", "Historical Floods",
        "land_cover_enc", "soil_type_enc",
        "is_monsoon", "is_summer", "is_cyclone_season", "year",
    ]
    TARGET_MULTI = ["flood_label", "cyclone_label", "landslide_label", "heatwave_label"]
    TARGET_SINGLE = "risk_label_enc"

    @st.cache_data(show_spinner=False)
    def train_model(model_name, n_est, data_hash):
        X = df[FEATURES]
        y_multi  = df[TARGET_MULTI]
        y_single = df[TARGET_SINGLE]

        X_train, X_test, ym_train, ym_test, ys_train, ys_test = train_test_split(
            X, y_multi, y_single, test_size=0.2, random_state=42
        )

        scaler = StandardScaler()
        X_train_s = scaler.fit_transform(X_train)
        X_test_s  = scaler.transform(X_test)

        base = (
            RandomForestClassifier(n_estimators=n_est, random_state=42, n_jobs=-1)
            if model_name == "Random Forest"
            else GradientBoostingClassifier(n_estimators=n_est, random_state=42)
        )

        # Multi-label (per-hazard)
        multi_clf = MultiOutputClassifier(base)
        multi_clf.fit(X_train_s, ym_train)
        ym_pred = multi_clf.predict(X_test_s)

        # Single-label (max risk)
        single_clf = (
            RandomForestClassifier(n_estimators=n_est, random_state=42, n_jobs=-1)
            if model_name == "Random Forest"
            else GradientBoostingClassifier(n_estimators=n_est, random_state=42)
        )
        single_clf.fit(X_train_s, ys_train)
        ys_pred = single_clf.predict(X_test_s)

        acc = accuracy_score(ys_test, ys_pred)

        # Feature importance (from single model)
        if model_name == "Random Forest":
            fi = single_clf.feature_importances_
        else:
            fi = single_clf.feature_importances_

        return {
            "scaler": scaler,
            "multi_clf": multi_clf,
            "single_clf": single_clf,
            "ym_test": ym_test,
            "ym_pred": ym_pred,
            "ys_test": ys_test,
            "ys_pred": ys_pred,
            "accuracy": acc,
            "fi": fi,
        }

    with st.spinner("🔄 Training ML models..."):
        result = train_model(model_choice, n_estimators, hash(tuple(df.shape)))

    acc = result["accuracy"]
    st.success(f"✅ Model trained! Overall Accuracy: **{acc*100:.2f}%**")

    mc1, mc2, mc3 = st.columns(3)
    mc1.metric("🎯 Overall Accuracy", f"{acc*100:.2f}%")
    mc2.metric("📦 Training Samples", f"{int(len(df)*0.8):,}")
    mc3.metric("🧪 Test Samples",     f"{int(len(df)*0.2):,}")

    # --- Per-hazard accuracy
    st.markdown('<div class="section-header">📈 Per-Hazard Model Performance</div>', unsafe_allow_html=True)
    hazard_names = ["Flood", "Cyclone", "Landslide", "Heatwave"]
    ym_test  = result["ym_test"]
    ym_pred  = result["ym_pred"]

    h_cols = st.columns(4)
    for i, (col, name) in enumerate(zip(h_cols, hazard_names)):
        hacc = accuracy_score(ym_test.iloc[:, i], ym_pred[:, i])
        col.metric(f"{name}", f"{hacc*100:.1f}%")

    # --- Feature Importance
    st.markdown('<div class="section-header">🔑 Feature Importance</div>', unsafe_allow_html=True)
    fi_df = pd.DataFrame({
        "Feature": FEATURES,
        "Importance": result["fi"],
    }).sort_values("Importance", ascending=True).tail(15)

    fig_fi = px.bar(
        fi_df, x="Importance", y="Feature", orientation="h",
        color="Importance", color_continuous_scale="Blues",
        title="Top Feature Importances (Overall Risk Classifier)",
    )
    fig_fi.update_layout(height=500, coloraxis_showscale=False)
    st.plotly_chart(fig_fi, use_container_width=True)

    # --- Confusion Matrix
    st.markdown('<div class="section-header">🔲 Confusion Matrix (Overall Risk)</div>', unsafe_allow_html=True)
    ys_test  = result["ys_test"]
    ys_pred  = result["ys_pred"]
    labels   = le_risk.classes_

    cm = confusion_matrix(ys_test, ys_pred)
    fig_cm = px.imshow(
        cm, text_auto=True,
        x=labels, y=labels,
        color_continuous_scale="Blues",
        title="Confusion Matrix",
    )
    fig_cm.update_layout(height=450)
    st.plotly_chart(fig_cm, use_container_width=True)

    # --- Classification Report
    st.markdown('<div class="section-header">📄 Classification Report</div>', unsafe_allow_html=True)
    report = classification_report(ys_test, ys_pred, target_names=labels, output_dict=True)
    report_df = pd.DataFrame(report).T.round(3)
    st.dataframe(report_df, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 4 — PREDICT MY RISK
# ══════════════════════════════════════════════════════════════════════════════
with tabs[3]:
    st.markdown('<div class="section-header">🔮 Real-Time Risk Predictor</div>', unsafe_allow_html=True)
    st.info("Enter environmental parameters for your location to get an instant disaster risk prediction.")

    with st.form("predict_form"):
        pc1, pc2, pc3 = st.columns(3)
        with pc1:
            p_rainfall   = st.number_input("🌧️ Rainfall (mm)",         0.0, 500.0, 120.0, 5.0)
            p_temp       = st.number_input("🌡️ Temperature (°C)",       0.0, 55.0, 32.0, 0.5)
            p_humidity   = st.number_input("💧 Humidity (%)",            0.0, 100.0, 70.0, 1.0)
            p_river_disc = st.number_input("🏞️ River Discharge (m³/s)", 0.0, 20000.0, 2000.0, 100.0)
            p_water_lvl  = st.number_input("📏 Water Level (m)",        0.0, 30.0, 5.0, 0.1)

        with pc2:
            p_elevation  = st.number_input("⛰️ Elevation (m)",          0.0, 9000.0, 300.0, 10.0)
            p_pop_den    = st.number_input("👥 Population Density",     100.0, 100000.0, 5000.0, 100.0)
            p_infra      = st.selectbox("🏗️ Infrastructure Quality",    [0, 1], format_func=lambda x: "Good" if x==1 else "Poor")
            p_hist_fl    = st.selectbox("📜 Historical Floods",         [0, 1], format_func=lambda x: "Yes" if x==1 else "No")
            p_land_cover = st.selectbox("🌿 Land Cover",                le_land.classes_.tolist())

        with pc3:
            p_soil_type  = st.selectbox("🪨 Soil Type",                 le_soil.classes_.tolist())
            p_monsoon    = st.selectbox("🌦️ Is Monsoon Season?",        [0, 1], format_func=lambda x: "Yes" if x==1 else "No")
            p_summer     = st.selectbox("☀️ Is Summer Season?",         [0, 1], format_func=lambda x: "Yes" if x==1 else "No")
            p_cyclone_s  = st.selectbox("🌀 Is Cyclone Season?",        [0, 1], format_func=lambda x: "Yes" if x==1 else "No")
            p_year       = st.number_input("📅 Year",                   2015, 2030, 2025, 1)

        predict_btn = st.form_submit_button("🚀 Predict My Risk", use_container_width=True)

    if predict_btn:
        try:
            scaler     = result["scaler"]
            single_clf = result["single_clf"]
            multi_clf  = result["multi_clf"]

            input_row = pd.DataFrame([{
                "Rainfall (mm)":            p_rainfall,
                "Temperature (°C)":         p_temp,
                "Humidity (%)":             p_humidity,
                "River Discharge (m³/s)":   p_river_disc,
                "Water Level (m)":          p_water_lvl,
                "Elevation (m)":            p_elevation,
                "Population Density":       p_pop_den,
                "Infrastructure":           p_infra,
                "Historical Floods":        p_hist_fl,
                "land_cover_enc":           le_land.transform([p_land_cover])[0],
                "soil_type_enc":            le_soil.transform([p_soil_type])[0],
                "is_monsoon":               p_monsoon,
                "is_summer":                p_summer,
                "is_cyclone_season":        p_cyclone_s,
                "year":                     p_year,
            }])

            X_in = scaler.transform(input_row[FEATURES])
            risk_enc  = single_clf.predict(X_in)[0]
            risk_label = le_risk.inverse_transform([risk_enc])[0]

            if hasattr(single_clf, "predict_proba"):
                proba = single_clf.predict_proba(X_in)[0]
                classes = le_risk.classes_
            else:
                proba = None
                classes = []

            multi_pred = multi_clf.predict(X_in)[0]

            # Result display
            st.markdown("---")
            risk_color = {
                "flood":        "#2980b9",
                "cyclone":      "#e67e22",
                "landslide":    "#27ae60",
                "heatwave":     "#e74c3c",
                "no_major_risk":"#95a5a6",
            }.get(risk_label, "#888")

            st.markdown(
                f'<div style="background:{risk_color};border-radius:14px;padding:1.5rem;'
                f'text-align:center;color:white;margin-bottom:1rem;">'
                f'<div style="font-size:2.5rem;font-weight:900">⚠️ {risk_label.replace("_"," ").title()}</div>'
                f'<div style="font-size:1rem;opacity:0.9;margin-top:0.4rem">Predicted Primary Hazard</div>'
                f'</div>',
                unsafe_allow_html=True,
            )

            # Per-hazard flags
            hc1, hc2, hc3, hc4 = st.columns(4)
            for col, name, val, emoji, color in [
                (hc1, "Flood",    multi_pred[0], "🌊", "#2980b9"),
                (hc2, "Cyclone",  multi_pred[1], "🌀", "#e67e22"),
                (hc3, "Landslide",multi_pred[2], "⛰️","#27ae60"),
                (hc4, "Heatwave", multi_pred[3], "🌡️","#e74c3c"),
            ]:
                bg = color if val == 1 else "#e0e0e0"
                tc = "white" if val == 1 else "#555"
                col.markdown(
                    f'<div style="background:{bg};border-radius:10px;padding:0.8rem;'
                    f'text-align:center;color:{tc};font-weight:700">'
                    f'{emoji} {name}<br><span style="font-size:1.3rem">'
                    f'{"⚠️ ALERT" if val==1 else "✅ Safe"}</span></div>',
                    unsafe_allow_html=True,
                )

            # Probability chart
            if proba is not None:
                st.markdown('<div class="section-header">📊 Risk Probability Breakdown</div>', unsafe_allow_html=True)
                prob_df = pd.DataFrame({"Risk Type": classes, "Probability": proba})
                prob_df["Probability %"] = (prob_df["Probability"] * 100).round(1)
                fig_prob = px.bar(
                    prob_df.sort_values("Probability", ascending=True),
                    x="Probability %", y="Risk Type", orientation="h",
                    color="Risk Type",
                    color_discrete_map=color_map,
                    title="Predicted Risk Probabilities",
                    text="Probability %",
                )
                fig_prob.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
                fig_prob.update_layout(showlegend=False, height=320)
                st.plotly_chart(fig_prob, use_container_width=True)

            # Advisory
            st.markdown('<div class="section-header">📢 Advisory & Actions</div>', unsafe_allow_html=True)
            advisories = {
                "flood":     ("alert-flood",    "🌊 FLOOD ALERT",
                              "Move to higher ground. Avoid flood plains and riverbanks. Keep emergency kit ready."),
                "cyclone":   ("alert-cyclone",  "🌀 CYCLONE ALERT",
                              "Stay indoors. Board windows. Evacuate coastal zones. Monitor IMD updates."),
                "landslide": ("alert-landslide","⛰️ LANDSLIDE ALERT",
                              "Avoid hillslopes and loose terrain. Do not cross rivers during heavy rain."),
                "heatwave":  ("alert-heatwave", "🌡️ HEATWAVE ALERT",
                              "Stay hydrated. Avoid outdoor activity between 11am–4pm. Wear light clothing."),
                "no_major_risk": ("", "✅ No Immediate Threat",
                                  "No major disaster risk detected. Continue monitoring local weather updates."),
            }
            cls_a, title_a, msg_a = advisories.get(risk_label, ("", "Unknown", ""))
            st.markdown(
                f'<div class="alert-box {cls_a}"><b>{title_a}</b><br>{msg_a}</div>',
                unsafe_allow_html=True,
            )

        except Exception as e:
            st.error(f"Prediction error: {e}. Please train the model first.")

# ══════════════════════════════════════════════════════════════════════════════
# TAB 5 — LANGUAGES
# ══════════════════════════════════════════════════════════════════════════════
# ══════════════════════════════════════════════════════════════════════════════
# TAB 4 — LIVE API DETECTION
# ══════════════════════════════════════════════════════════════════════════════
with tabs[4]:
    st.markdown('<div class="section-header">🌤️ Live Weather API — Real-Time Disaster Detection</div>', unsafe_allow_html=True)
    st.info(
        "Enter your **OpenWeatherMap API key** to fetch live weather data for any Indian city and "
        "run the HazardNet ML model on real-time conditions. "
        "Get a free key at [openweathermap.org](https://openweathermap.org/api)"
    )

    import requests
    import datetime

    # ── API key input ────────────────────────────────────────────────────────
    api_col1, api_col2 = st.columns([3, 1])
    with api_col1:
        owm_key = st.text_input(
            "🔑 OpenWeatherMap API Key",
            type="password",
            placeholder="Paste your free API key here...",
            help="Free tier supports 60 calls/min — enough for this dashboard",
        )
    with api_col2:
        api_city = st.selectbox(
            "🏙️ City",
            ["Chennai", "Mumbai", "Kolkata", "Kochi", "Hyderabad",
             "Bhubaneswar", "Guwahati", "Jaipur", "Delhi", "Bengaluru",
             "Pune", "Ahmedabad", "Visakhapatnam", "Patna", "Bhopal"],
        )

    fetch_btn = st.button("🚀 Fetch Live Weather & Predict Risk", use_container_width=True)

    # ── Demo / fallback data per city ────────────────────────────────────────
    CITY_DEMO = {
        "Chennai":      {"lat": 13.08, "lon": 80.27, "rain": 85,  "temp": 34, "hum": 78, "ws": 18},
        "Mumbai":       {"lat": 19.08, "lon": 72.88, "rain": 120, "temp": 30, "hum": 85, "ws": 22},
        "Kolkata":      {"lat": 22.57, "lon": 88.36, "rain": 60,  "temp": 33, "hum": 80, "ws": 15},
        "Kochi":        {"lat": 9.93,  "lon": 76.26, "rain": 200, "temp": 28, "hum": 90, "ws": 12},
        "Hyderabad":    {"lat": 17.38, "lon": 78.49, "rain": 10,  "temp": 42, "hum": 35, "ws": 8},
        "Bhubaneswar":  {"lat": 20.30, "lon": 85.82, "rain": 50,  "temp": 35, "hum": 72, "ws": 30},
        "Guwahati":     {"lat": 26.14, "lon": 91.74, "rain": 180, "temp": 29, "hum": 88, "ws": 10},
        "Jaipur":       {"lat": 26.91, "lon": 75.79, "rain": 2,   "temp": 44, "hum": 20, "ws": 6},
        "Delhi":        {"lat": 28.61, "lon": 77.21, "rain": 5,   "temp": 40, "hum": 30, "ws": 9},
        "Bengaluru":    {"lat": 12.97, "lon": 77.59, "rain": 30,  "temp": 27, "hum": 65, "ws": 7},
        "Pune":         {"lat": 18.52, "lon": 73.86, "rain": 45,  "temp": 31, "hum": 70, "ws": 11},
        "Ahmedabad":    {"lat": 23.03, "lon": 72.58, "rain": 3,   "temp": 43, "hum": 25, "ws": 8},
        "Visakhapatnam":{"lat": 17.69, "lon": 83.22, "rain": 70,  "temp": 33, "hum": 75, "ws": 25},
        "Patna":        {"lat": 25.59, "lon": 85.14, "rain": 90,  "temp": 36, "hum": 82, "ws": 14},
        "Bhopal":       {"lat": 23.25, "lon": 77.41, "rain": 20,  "temp": 38, "hum": 45, "ws": 10},
    }

    def fetch_owm(city, key):
        """Fetch current weather from OpenWeatherMap."""
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city},IN&appid={key}&units=metric"
        r = requests.get(url, timeout=8)
        if r.status_code == 200:
            d = r.json()
            return {
                "lat":  d["coord"]["lat"],
                "lon":  d["coord"]["lon"],
                "temp": d["main"]["temp"],
                "hum":  d["main"]["humidity"],
                "ws":   d["wind"]["speed"],
                "rain": d.get("rain", {}).get("1h", 0) * 24,  # scale to daily mm
                "desc": d["weather"][0]["description"].title(),
                "icon": d["weather"][0]["icon"],
                "feels_like": d["main"]["feels_like"],
                "pressure":   d["main"]["pressure"],
                "visibility": d.get("visibility", 10000) / 1000,
            }
        return None

    def fetch_forecast(city, key):
        """Fetch 5-day 3-hour forecast from OpenWeatherMap."""
        url = f"https://api.openweathermap.org/data/2.5/forecast?q={city},IN&appid={key}&units=metric&cnt=40"
        r = requests.get(url, timeout=8)
        if r.status_code == 200:
            d = r.json()
            rows = []
            for item in d["list"]:
                rows.append({
                    "datetime": item["dt_txt"],
                    "temp":     item["main"]["temp"],
                    "humidity": item["main"]["humidity"],
                    "rain":     item.get("rain", {}).get("3h", 0),
                    "desc":     item["weather"][0]["description"].title(),
                })
            return pd.DataFrame(rows)
        return None

    def run_api_prediction(weather, city, model_result, le_land, le_soil, le_risk, df):
        """Run the trained ML model on live weather data."""
        try:
            # Estimate river discharge and water level from rainfall
            est_river = max(500, weather["rain"] * 30)
            est_water = max(1.0, weather["rain"] / 15)
            # Elevation from dataset median near city
            cd = CITY_DEMO[city]
            subset = df[
                (df["Latitude"].between(cd["lat"] - 2, cd["lat"] + 2)) &
                (df["Longitude"].between(cd["lon"] - 2, cd["lon"] + 2))
            ]
            elev = subset["Elevation (m)"].median() if not subset.empty else 150.0
            pop  = subset["Population Density"].median() if not subset.empty else 8000.0

            now = datetime.datetime.now()
            month = now.month
            is_monsoon     = 1 if month in [6, 7, 8, 9] else 0
            is_summer      = 1 if month in [3, 4, 5] else 0
            is_cyclone_s   = 1 if month in [10, 11, 12, 4, 5] else 0

            input_row = pd.DataFrame([{
                "Rainfall (mm)":          weather["rain"],
                "Temperature (°C)":       weather["temp"],
                "Humidity (%)":           weather["hum"],
                "River Discharge (m³/s)": est_river,
                "Water Level (m)":        est_water,
                "Elevation (m)":          elev,
                "Population Density":     pop,
                "Infrastructure":         1,
                "Historical Floods":      1,
                "land_cover_enc":         le_land.transform(["Urban"])[0],
                "soil_type_enc":          le_soil.transform(["Clay"])[0],
                "is_monsoon":             is_monsoon,
                "is_summer":              is_summer,
                "is_cyclone_season":      is_cyclone_s,
                "year":                   now.year,
            }])

            FEATURES = [
                "Rainfall (mm)", "Temperature (°C)", "Humidity (%)",
                "River Discharge (m³/s)", "Water Level (m)", "Elevation (m)",
                "Population Density", "Infrastructure", "Historical Floods",
                "land_cover_enc", "soil_type_enc",
                "is_monsoon", "is_summer", "is_cyclone_season", "year",
            ]

            scaler     = model_result["scaler"]
            single_clf = model_result["single_clf"]
            multi_clf  = model_result["multi_clf"]

            X_in = scaler.transform(input_row[FEATURES])
            risk_enc   = single_clf.predict(X_in)[0]
            risk_label = le_risk.inverse_transform([risk_enc])[0]
            proba      = single_clf.predict_proba(X_in)[0]
            classes    = le_risk.classes_
            multi_pred = multi_clf.predict(X_in)[0]

            return risk_label, proba, classes, multi_pred, input_row
        except Exception as e:
            return None, None, None, None, None

    # ── Main fetch & display ─────────────────────────────────────────────────
    use_demo = False
    weather_data = None

    if fetch_btn:
        if owm_key.strip():
            with st.spinner(f"📡 Fetching live weather for {api_city}..."):
                weather_data = fetch_owm(api_city, owm_key.strip())
            if weather_data is None:
                st.error("❌ API call failed. Check your API key or try again. Showing demo data.")
                use_demo = True
            else:
                st.success(f"✅ Live weather fetched for **{api_city}**!")
        else:
            st.warning("⚠️ No API key entered — showing **demo simulation** data.")
            use_demo = True

        if use_demo:
            cd = CITY_DEMO[api_city]
            weather_data = {
                "lat": cd["lat"], "lon": cd["lon"],
                "temp": cd["temp"], "hum": cd["hum"],
                "ws": cd["ws"], "rain": cd["rain"],
                "desc": "Demo Simulation", "icon": "10d",
                "feels_like": cd["temp"] - 2,
                "pressure": 1008, "visibility": 8.0,
            }

        if weather_data:
            # ── Weather cards ────────────────────────────────────────────────
            st.markdown('<div class="section-header">🌡️ Current Conditions</div>', unsafe_allow_html=True)
            wc1, wc2, wc3, wc4, wc5, wc6 = st.columns(6)
            for col, icon, label, val in [
                (wc1, "🌧️", "Rainfall (mm/day)",   f"{weather_data['rain']:.1f}"),
                (wc2, "🌡️", "Temperature (°C)",     f"{weather_data['temp']:.1f}"),
                (wc3, "💧", "Humidity (%)",          f"{weather_data['hum']}"),
                (wc4, "💨", "Wind Speed (m/s)",      f"{weather_data['ws']}"),
                (wc5, "📊", "Pressure (hPa)",        f"{weather_data['pressure']}"),
                (wc6, "👁️", "Visibility (km)",       f"{weather_data['visibility']:.1f}"),
            ]:
                col.markdown(
                    f'<div class="metric-card"><div style="font-size:1.6rem">{icon}</div>'
                    f'<div class="metric-value" style="font-size:1.5rem">{val}</div>'
                    f'<div class="metric-label">{label}</div></div>',
                    unsafe_allow_html=True,
                )

            # ── ML Prediction on live data ───────────────────────────────────
            st.markdown('<div class="section-header">🤖 Live ML Risk Prediction</div>', unsafe_allow_html=True)

            try:
                model_res = train_model(model_choice, n_estimators, hash(tuple(df.shape)))
                risk_label, proba, classes, multi_pred, inp_row = run_api_prediction(
                    weather_data, api_city, model_res, le_land, le_soil, le_risk, df
                )

                if risk_label:
                    hazard_color_map = {
                        "flood": "#2980b9", "cyclone": "#e67e22",
                        "landslide": "#27ae60", "heatwave": "#e74c3c",
                        "no_major_risk": "#27ae60",
                    }
                    rc = hazard_color_map.get(risk_label, "#888")

                    st.markdown(
                        f'<div style="background:{rc};border-radius:16px;padding:1.5rem;'
                        f'text-align:center;color:white;margin-bottom:1rem;">'
                        f'<div style="font-size:0.9rem;opacity:0.85">🏙️ {api_city} — Live Prediction</div>'
                        f'<div style="font-size:2.4rem;font-weight:900;margin:0.3rem 0">'
                        f'⚠️ {risk_label.replace("_"," ").title()}</div>'
                        f'<div style="font-size:0.85rem;opacity:0.8">'
                        f'Conditions: {weather_data["desc"]} | {datetime.datetime.now().strftime("%d %b %Y %H:%M")}'
                        f'</div></div>',
                        unsafe_allow_html=True,
                    )

                    # Per-hazard flags
                    ph1, ph2, ph3, ph4 = st.columns(4)
                    for col, name, val, emoji, color in [
                        (ph1, "Flood",     multi_pred[0], "🌊", "#2980b9"),
                        (ph2, "Cyclone",   multi_pred[1], "🌀", "#e67e22"),
                        (ph3, "Landslide", multi_pred[2], "⛰️", "#27ae60"),
                        (ph4, "Heatwave",  multi_pred[3], "🌡️", "#e74c3c"),
                    ]:
                        bg = color if val == 1 else "#e8e8e8"
                        tc = "white" if val == 1 else "#555"
                        col.markdown(
                            f'<div style="background:{bg};border-radius:10px;padding:0.8rem;'
                            f'text-align:center;color:{tc};font-weight:700;margin-bottom:0.5rem">'
                            f'{emoji} {name}<br><span style="font-size:1.2rem">'
                            f'{"⚠️ ALERT" if val==1 else "✅ Safe"}</span></div>',
                            unsafe_allow_html=True,
                        )

                    # Probability bar chart
                    if proba is not None:
                        prob_df = pd.DataFrame({
                            "Risk Type": classes,
                            "Probability %": (proba * 100).round(1)
                        }).sort_values("Probability %", ascending=True)
                        fig_prob = px.bar(
                            prob_df, x="Probability %", y="Risk Type", orientation="h",
                            color="Risk Type",
                            color_discrete_map={
                                "flood":"#2980b9","cyclone":"#e67e22",
                                "landslide":"#27ae60","heatwave":"#e74c3c","no_major_risk":"#95a5a6"
                            },
                            title=f"Risk Probability Breakdown — {api_city}",
                            text="Probability %",
                        )
                        fig_prob.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
                        fig_prob.update_layout(showlegend=False, height=300)
                        st.plotly_chart(fig_prob, use_container_width=True)

            except Exception as e:
                st.error(f"Prediction error: {e}. Please visit ML Prediction tab first to train the model.")

            # ── 5-Day Forecast (live or simulated) ──────────────────────────
            st.markdown('<div class="section-header">📅 5-Day Risk Forecast (Simulated Trend)</div>', unsafe_allow_html=True)

            forecast_days = []
            base_rain = weather_data["rain"]
            base_temp = weather_data["temp"]
            for i in range(5):
                day = datetime.datetime.now() + datetime.timedelta(days=i)
                rain_v = max(0, base_rain + np.random.uniform(-30, 40))
                temp_v = base_temp + np.random.uniform(-2, 3)
                flood_r    = min(100, rain_v * 0.6 + weather_data["hum"] * 0.2)
                cyclone_r  = min(100, weather_data["ws"] * 2.5 + rain_v * 0.3)
                heatwave_r = min(100, max(0, temp_v - 35) * 8)
                landslide_r= min(100, rain_v * 0.4 + 10)
                forecast_days.append({
                    "Day": day.strftime("%a %d %b"),
                    "Rainfall (mm)": round(rain_v, 1),
                    "Temp (°C)":     round(temp_v, 1),
                    "Flood Risk %":      round(flood_r, 1),
                    "Cyclone Risk %":    round(cyclone_r, 1),
                    "Heatwave Risk %":   round(heatwave_r, 1),
                    "Landslide Risk %":  round(landslide_r, 1),
                })

            fc_df = pd.DataFrame(forecast_days)
            fig_fc = px.line(
                fc_df, x="Day",
                y=["Flood Risk %", "Cyclone Risk %", "Heatwave Risk %", "Landslide Risk %"],
                markers=True,
                title=f"5-Day Hazard Risk Trend — {api_city}",
                color_discrete_map={
                    "Flood Risk %": "#2980b9", "Cyclone Risk %": "#e67e22",
                    "Heatwave Risk %": "#e74c3c", "Landslide Risk %": "#27ae60",
                },
            )
            fig_fc.update_layout(height=350, yaxis_title="Risk Score (%)", legend_title="Hazard")
            st.plotly_chart(fig_fc, use_container_width=True)
            st.dataframe(fc_df, use_container_width=True, hide_index=True)

            # ── City location map ────────────────────────────────────────────
            st.markdown('<div class="section-header">📍 Location Map</div>', unsafe_allow_html=True)
            loc_df = pd.DataFrame([{
                "City": api_city,
                "lat": weather_data["lat"],
                "lon": weather_data["lon"],
                "Risk": risk_label if "risk_label" in dir() else "unknown",
            }])
            fig_loc = px.scatter_mapbox(
                loc_df, lat="lat", lon="lon",
                hover_name="City",
                zoom=8, mapbox_style="carto-positron",
                size_max=20,
                title=f"{api_city} — Live Risk Location",
            )
            fig_loc.update_traces(marker=dict(size=18, color="#e74c3c"))
            fig_loc.update_layout(height=400, margin=dict(l=0, r=0, t=40, b=0))
            st.plotly_chart(fig_loc, use_container_width=True)

    else:
        st.markdown("""
        <div style="background:#f0f4f8;border-radius:14px;padding:2rem;text-align:center;color:#555;">
            <div style="font-size:3rem">🌐</div>
            <div style="font-size:1.2rem;font-weight:700;margin-top:0.5rem">Ready to fetch live data</div>
            <div style="margin-top:0.5rem">Enter an API key and click <b>Fetch Live Weather & Predict Risk</b>
            — or leave blank for demo simulation.</div>
            <div style="margin-top:1rem;font-size:0.85rem;color:#888">
            Free API key: <a href="https://openweathermap.org/api" target="_blank">openweathermap.org/api</a>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="section-header">📡 API Architecture</div>', unsafe_allow_html=True)
        api_flow = pd.DataFrame([
            {"Step": "1. GPS / City Input",    "Source": "User / Mobile GPS",      "Data": "Lat, Lon, City name"},
            {"Step": "2. Weather Fetch",        "Source": "OpenWeatherMap API",     "Data": "Rain, Temp, Humidity, Wind"},
            {"Step": "3. Satellite Data",       "Source": "NASA POWER API",         "Data": "Solar radiation, Soil moisture"},
            {"Step": "4. River Data",           "Source": "IMD / NDMA",             "Data": "River discharge, Water level"},
            {"Step": "5. Feature Engineering", "Source": "HazardNet Engine",        "Data": "Kriging, Season flags, History"},
            {"Step": "6. ML Ensemble",          "Source": "XGBoost + LSTM + TFT",   "Data": "Risk scores per hazard type"},
            {"Step": "7. Alert Generation",     "Source": "HazardNet Backend",      "Data": "Risk label + SHAP explanation"},
            {"Step": "8. Multilingual Alert",   "Source": "Translation Engine",     "Data": "Alert in user's regional language"},
        ])
        st.dataframe(api_flow, use_container_width=True, hide_index=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 5 — SOS ADMIN DASHBOARD
# ══════════════════════════════════════════════════════════════════════════════
with tabs[5]:
    st.markdown('<div class="section-header">🚨 SOS Admin Dashboard — Emergency Command Center</div>', unsafe_allow_html=True)

    # ── Admin Login ──────────────────────────────────────────────────────────
    if "admin_logged_in" not in st.session_state:
        st.session_state.admin_logged_in = False
    if "sos_alerts" not in st.session_state:
        st.session_state.sos_alerts = []
    if "resources" not in st.session_state:
        st.session_state.resources = {
            "Relief Camps":      {"total": 45, "active": 12, "capacity": 5000},
            "Rescue Teams":      {"total": 120, "active": 38, "capacity": 760},
            "Medical Units":     {"total": 30,  "active": 9,  "capacity": 270},
            "Helicopters":       {"total": 8,   "active": 3,  "capacity": 24},
            "Boats":             {"total": 95,  "active": 22, "capacity": 440},
            "Food Packets (k)":  {"total": 500, "active": 180,"capacity": 180000},
        }

    if not st.session_state.admin_logged_in:
        st.warning("🔐 Admin access required. Please log in.")
        lc1, lc2, lc3 = st.columns([1, 2, 1])
        with lc2:
            st.markdown("### 🔑 Admin Login")
            admin_user = st.text_input("Username", placeholder="admin")
            admin_pass = st.text_input("Password", type="password", placeholder="••••••••")
            if st.button("🔓 Login", use_container_width=True):
                if admin_user == "admin" and admin_pass == "hazardnet123":
                    st.session_state.admin_logged_in = True
                    st.rerun()
                else:
                    st.error("❌ Invalid credentials. Use admin / hazardnet123")
            st.caption("Demo credentials — username: `admin` | password: `hazardnet123`")
    else:
        # ── Top bar ──────────────────────────────────────────────────────────
        ab1, ab2 = st.columns([6, 1])
        with ab2:
            if st.button("🔒 Logout"):
                st.session_state.admin_logged_in = False
                st.rerun()
        with ab1:
            st.success(f"✅ Logged in as **Admin** | {datetime.datetime.now().strftime('%d %b %Y  %H:%M:%S')}")

        # ── Seed demo SOS alerts ─────────────────────────────────────────────
        if not st.session_state.sos_alerts:
            st.session_state.sos_alerts = [
                {
                    "id": "SOS-001", "time": "08:14 AM", "city": "Chennai",
                    "lat": 13.08, "lon": 80.27, "hazard": "flood",
                    "severity": "CRITICAL", "status": "Pending",
                    "name": "Rajesh Kumar", "phone": "+91-9876543210",
                    "message": "Water level rising fast. House flooded. 4 people trapped.",
                    "rescue_team": "RT-Chennai-01",
                },
                {
                    "id": "SOS-002", "time": "08:32 AM", "city": "Kochi",
                    "lat": 9.93, "lon": 76.26, "hazard": "landslide",
                    "severity": "HIGH", "status": "Dispatched",
                    "name": "Priya Menon", "phone": "+91-9845678901",
                    "message": "Landslide blocked road. Elderly couple needs medical help.",
                    "rescue_team": "RT-Kochi-02",
                },
                {
                    "id": "SOS-003", "time": "09:05 AM", "city": "Bhubaneswar",
                    "lat": 20.30, "lon": 85.82, "hazard": "cyclone",
                    "severity": "CRITICAL", "status": "Resolved",
                    "name": "Suresh Patnaik", "phone": "+91-9437654321",
                    "message": "Roof collapsed. Family of 6 stranded. Need immediate rescue.",
                    "rescue_team": "RT-ODISHA-01",
                },
                {
                    "id": "SOS-004", "time": "09:48 AM", "city": "Jaipur",
                    "lat": 26.91, "lon": 75.79, "hazard": "heatwave",
                    "severity": "MEDIUM", "status": "Pending",
                    "name": "Meena Sharma", "phone": "+91-9414567890",
                    "message": "Elderly man collapsed due to heat. Need ambulance.",
                    "rescue_team": "Unassigned",
                },
                {
                    "id": "SOS-005", "time": "10:15 AM", "city": "Guwahati",
                    "lat": 26.14, "lon": 91.74, "hazard": "flood",
                    "severity": "HIGH", "status": "Dispatched",
                    "name": "Dipankar Borah", "phone": "+91-9954321678",
                    "message": "Brahmaputra flooding. Village submerged. 50+ people on rooftops.",
                    "rescue_team": "RT-Assam-03",
                },
                {
                    "id": "SOS-006", "time": "10:52 AM", "city": "Mumbai",
                    "lat": 19.08, "lon": 72.88, "hazard": "flood",
                    "severity": "HIGH", "status": "Pending",
                    "name": "Anjali Desai", "phone": "+91-9867452301",
                    "message": "Underpass flooded. Car stuck. Driver trapped inside.",
                    "rescue_team": "Unassigned",
                },
            ]

        alerts_df = pd.DataFrame(st.session_state.sos_alerts)

        # ── KPI Cards ─────────────────────────────────────────────────────────
        st.markdown('<div class="section-header">📊 Emergency Overview</div>', unsafe_allow_html=True)
        k1, k2, k3, k4, k5, k6 = st.columns(6)
        total_sos    = len(alerts_df)
        critical_sos = len(alerts_df[alerts_df["severity"] == "CRITICAL"])
        pending_sos  = len(alerts_df[alerts_df["status"] == "Pending"])
        dispatch_sos = len(alerts_df[alerts_df["status"] == "Dispatched"])
        resolved_sos = len(alerts_df[alerts_df["status"] == "Resolved"])
        active_res   = st.session_state.resources["Rescue Teams"]["active"]

        for col, label, val, color in [
            (k1, "🚨 Total SOS",     total_sos,    "#e74c3c"),
            (k2, "🔴 Critical",      critical_sos, "#c0392b"),
            (k3, "⏳ Pending",       pending_sos,  "#e67e22"),
            (k4, "🚁 Dispatched",    dispatch_sos, "#2980b9"),
            (k5, "✅ Resolved",      resolved_sos, "#27ae60"),
            (k6, "👥 Active Teams",  active_res,   "#8e44ad"),
        ]:
            col.markdown(
                f'<div class="metric-card" style="background:{color}">'
                f'<div class="metric-value">{val}</div>'
                f'<div class="metric-label">{label}</div></div>',
                unsafe_allow_html=True,
            )

        # ── SOS Alert Table with Actions ──────────────────────────────────────
        st.markdown('<div class="section-header">🆘 Live SOS Alerts</div>', unsafe_allow_html=True)

        sev_filter = st.multiselect(
            "Filter by Severity",
            ["CRITICAL", "HIGH", "MEDIUM"],
            default=["CRITICAL", "HIGH", "MEDIUM"],
        )
        stat_filter = st.multiselect(
            "Filter by Status",
            ["Pending", "Dispatched", "Resolved"],
            default=["Pending", "Dispatched", "Resolved"],
        )

        filtered_alerts = alerts_df[
            alerts_df["severity"].isin(sev_filter) &
            alerts_df["status"].isin(stat_filter)
        ]

        sev_color = {"CRITICAL": "#e74c3c", "HIGH": "#e67e22", "MEDIUM": "#f1c40f"}
        stat_color = {"Pending": "#e74c3c", "Dispatched": "#2980b9", "Resolved": "#27ae60"}
        hazard_emoji = {"flood": "🌊", "cyclone": "🌀", "landslide": "⛰️", "heatwave": "🌡️"}

        for _, row in filtered_alerts.iterrows():
            sc = sev_color.get(row["severity"], "#888")
            stc = stat_color.get(row["status"], "#888")
            hemoji = hazard_emoji.get(row["hazard"], "⚠️")

            with st.expander(
                f"{hemoji} [{row['id']}] {row['city']} — {row['severity']} | {row['status']} | {row['time']}",
                expanded=(row["severity"] == "CRITICAL" and row["status"] == "Pending"),
            ):
                ec1, ec2 = st.columns([3, 2])
                with ec1:
                    st.markdown(f"""
                    <div style="background:#f8f9fa;border-radius:10px;padding:1rem;border-left:5px solid {sc}">
                        <b>👤 {row['name']}</b> | 📞 {row['phone']}<br>
                        🏙️ <b>{row['city']}</b> | {hemoji} <b>{row['hazard'].title()}</b><br>
                        ⏰ Reported: <b>{row['time']}</b><br>
                        👷 Rescue Team: <b>{row['rescue_team']}</b><br><br>
                        📢 <i>"{row['message']}"</i>
                    </div>
                    """, unsafe_allow_html=True)

                with ec2:
                    st.markdown(f"""
                    <div style="display:flex;gap:0.5rem;flex-wrap:wrap;margin-bottom:0.5rem">
                        <span style="background:{sc};color:white;padding:0.3rem 0.8rem;
                              border-radius:20px;font-weight:700;font-size:0.8rem">{row['severity']}</span>
                        <span style="background:{stc};color:white;padding:0.3rem 0.8rem;
                              border-radius:20px;font-weight:700;font-size:0.8rem">{row['status']}</span>
                    </div>
                    """, unsafe_allow_html=True)

                    new_status = st.selectbox(
                        "Update Status",
                        ["Pending", "Dispatched", "Resolved"],
                        index=["Pending", "Dispatched", "Resolved"].index(row["status"]),
                        key=f"status_{row['id']}",
                    )
                    new_team = st.text_input(
                        "Assign Rescue Team",
                        value=row["rescue_team"],
                        key=f"team_{row['id']}",
                    )
                    if st.button(f"💾 Update {row['id']}", key=f"upd_{row['id']}"):
                        for i, a in enumerate(st.session_state.sos_alerts):
                            if a["id"] == row["id"]:
                                st.session_state.sos_alerts[i]["status"]       = new_status
                                st.session_state.sos_alerts[i]["rescue_team"]  = new_team
                        st.success(f"✅ {row['id']} updated!")
                        st.rerun()

        # ── New SOS Entry ─────────────────────────────────────────────────────
        st.markdown('<div class="section-header">➕ Log New SOS Alert</div>', unsafe_allow_html=True)
        with st.expander("📋 Add Manual SOS Entry"):
            nc1, nc2, nc3 = st.columns(3)
            with nc1:
                n_name    = st.text_input("👤 Caller Name")
                n_phone   = st.text_input("📞 Phone Number")
                n_city    = st.selectbox("🏙️ City", list(city_coords.keys())[1:])
            with nc2:
                n_hazard  = st.selectbox("⚠️ Hazard Type", ["flood", "cyclone", "landslide", "heatwave"])
                n_sev     = st.selectbox("🔴 Severity", ["CRITICAL", "HIGH", "MEDIUM"])
                n_team    = st.text_input("👷 Rescue Team", "Unassigned")
            with nc3:
                n_msg     = st.text_area("📢 Message / Situation")

            if st.button("🚨 Log SOS Alert", use_container_width=True):
                if n_name and n_msg:
                    new_id = f"SOS-{len(st.session_state.sos_alerts)+1:03d}"
                    coords = city_coords.get(n_city, (20.0, 78.0))
                    st.session_state.sos_alerts.append({
                        "id": new_id,
                        "time": datetime.datetime.now().strftime("%I:%M %p"),
                        "city": n_city,
                        "lat": coords[0] if coords else 20.0,
                        "lon": coords[1] if coords else 78.0,
                        "hazard": n_hazard,
                        "severity": n_sev,
                        "status": "Pending",
                        "name": n_name,
                        "phone": n_phone,
                        "message": n_msg,
                        "rescue_team": n_team,
                    })
                    st.success(f"✅ {new_id} logged successfully!")
                    st.rerun()
                else:
                    st.warning("Please fill Name and Message fields.")

        # ── SOS Map ───────────────────────────────────────────────────────────
        st.markdown('<div class="section-header">🗺️ SOS Incident Map</div>', unsafe_allow_html=True)
        map_df = pd.DataFrame(st.session_state.sos_alerts)
        if not map_df.empty:
            map_df["color_key"] = map_df["severity"].map(
                {"CRITICAL": "red", "HIGH": "orange", "MEDIUM": "yellow"}
            )
            fig_sos_map = px.scatter_mapbox(
                map_df,
                lat="lat", lon="lon",
                color="severity",
                color_discrete_map={"CRITICAL": "#e74c3c", "HIGH": "#e67e22", "MEDIUM": "#f1c40f"},
                size_max=18,
                zoom=4,
                mapbox_style="carto-positron",
                hover_name="id",
                hover_data=["city", "hazard", "name", "status"],
                title="Live SOS Incident Locations",
            )
            fig_sos_map.update_traces(marker=dict(size=16))
            fig_sos_map.update_layout(height=480, margin=dict(l=0, r=0, t=40, b=0))
            st.plotly_chart(fig_sos_map, use_container_width=True)

        # ── Resource Management ───────────────────────────────────────────────
        st.markdown('<div class="section-header">🏕️ Resource Management</div>', unsafe_allow_html=True)
        res_data = []
        for res_name, res_vals in st.session_state.resources.items():
            pct = (res_vals["active"] / res_vals["total"] * 100) if res_vals["total"] > 0 else 0
            res_data.append({
                "Resource": res_name,
                "Total": res_vals["total"],
                "Active / Deployed": res_vals["active"],
                "Available": res_vals["total"] - res_vals["active"],
                "Utilization %": round(pct, 1),
            })
        res_df = pd.DataFrame(res_data)

        rc1, rc2 = st.columns(2)
        with rc1:
            fig_res = px.bar(
                res_df, x="Resource", y=["Active / Deployed", "Available"],
                barmode="stack", color_discrete_map={
                    "Active / Deployed": "#e74c3c",
                    "Available": "#27ae60",
                },
                title="Resource Deployment Status",
            )
            fig_res.update_layout(height=350, legend_title="")
            st.plotly_chart(fig_res, use_container_width=True)

        with rc2:
            fig_util = px.bar(
                res_df, x="Resource", y="Utilization %",
                color="Utilization %",
                color_continuous_scale="RdYlGn_r",
                title="Resource Utilization %",
                text="Utilization %",
            )
            fig_util.update_traces(texttemplate="%{text:.0f}%", textposition="outside")
            fig_util.update_layout(height=350, coloraxis_showscale=False)
            st.plotly_chart(fig_util, use_container_width=True)

        st.dataframe(res_df, use_container_width=True, hide_index=True)

        # ── Live update resource numbers ──────────────────────────────────────
        st.markdown('<div class="section-header">✏️ Update Resource Counts</div>', unsafe_allow_html=True)
        with st.expander("🔧 Edit Resource Deployment"):
            for res_name in st.session_state.resources:
                rc_col1, rc_col2 = st.columns(2)
                with rc_col1:
                    new_total = st.number_input(
                        f"{res_name} — Total",
                        min_value=0,
                        value=st.session_state.resources[res_name]["total"],
                        key=f"tot_{res_name}",
                    )
                with rc_col2:
                    new_active = st.number_input(
                        f"{res_name} — Deployed",
                        min_value=0,
                        max_value=new_total,
                        value=min(st.session_state.resources[res_name]["active"], new_total),
                        key=f"act_{res_name}",
                    )
                st.session_state.resources[res_name]["total"]  = new_total
                st.session_state.resources[res_name]["active"] = new_active

        # ── Broadcast Alert ────────────────────────────────────────────────────
        st.markdown('<div class="section-header">📢 Broadcast Emergency Alert</div>', unsafe_allow_html=True)
        with st.expander("📡 Send Broadcast to Field Teams & Public"):
            bc1, bc2 = st.columns(2)
            with bc1:
                bc_hazard   = st.selectbox("⚠️ Hazard Type", ["flood", "cyclone", "landslide", "heatwave"], key="bc_haz")
                bc_severity = st.selectbox("🔴 Severity Level", ["CRITICAL", "HIGH", "MEDIUM"], key="bc_sev")
                bc_city     = st.selectbox("🏙️ Target City", list(city_coords.keys())[1:], key="bc_city")
            with bc2:
                bc_msg = st.text_area(
                    "📢 Alert Message",
                    value=f"HAZARDNET ALERT: {bc_hazard.upper()} WARNING issued for area. "
                          "All residents move to higher ground. Rescue teams activated.",
                    key="bc_msg",
                    height=130,
                )
            bc_langs = st.multiselect(
                "🌐 Broadcast Languages",
                ["English", "Hindi (हिन्दी)", "Tamil (தமிழ்)", "Telugu (తెలుగు)",
                 "Malayalam (മലയാളം)", "Kannada (ಕನ್ನಡ)", "Bengali (বাংলা)", "Odia (ଓଡ଼ିଆ)"],
                default=["English", "Hindi (हिन्दी)"],
                key="bc_langs",
            )

            if st.button("📡 BROADCAST NOW", use_container_width=True):
                st.success(
                    f"✅ Alert broadcast sent!\n\n"
                    f"**City:** {bc_city} | **Hazard:** {bc_hazard.title()} | "
                    f"**Severity:** {bc_severity}\n\n"
                    f"**Languages:** {', '.join(bc_langs)}\n\n"
                    f"**Message:** {bc_msg}"
                )
                st.balloons()

        # ── Download report ────────────────────────────────────────────────────
        st.markdown("---")
        report_csv = pd.DataFrame(st.session_state.sos_alerts).to_csv(index=False).encode("utf-8")
        st.download_button(
            "⬇️ Download Full SOS Report (CSV)",
            report_csv, "hazardnet_sos_report.csv", "text/csv",
            use_container_width=True,
        )

with tabs[6]:
    st.markdown('<div class="section-header">🌐 Multilingual Early Warning System</div>', unsafe_allow_html=True)
    st.info("HazardNet India supports **16 languages** — English + 15 Indian regional languages. "
            "Select a hazard and language to preview the alert message as it would appear on a user's device.")

    # ── Full translations dictionary ──────────────────────────────────────────
    TRANSLATIONS = {
        "English": {
            "flag": "🇬🇧", "script": "Latin",
            "flood":     {
                "title":   "⚠️ FLOOD ALERT",
                "message": "Heavy flooding detected in your area. Move to higher ground immediately. "
                           "Avoid flood plains, riverbanks, and low-lying roads. Keep emergency kit ready.",
                "safe":    "✅ No flood risk detected in your area. Stay alert and monitor local weather.",
            },
            "cyclone":   {
                "title":   "🌀 CYCLONE ALERT",
                "message": "A cyclone is approaching your region. Stay indoors, board windows, "
                           "evacuate coastal zones immediately. Monitor IMD bulletins.",
                "safe":    "✅ No cyclone risk detected in your area. Stay alert and monitor local weather.",
            },
            "landslide": {
                "title":   "⛰️ LANDSLIDE ALERT",
                "message": "Landslide risk is HIGH. Avoid hillslopes and loose terrain. "
                           "Do not cross rivers or streams. Move to safe shelter now.",
                "safe":    "✅ No landslide risk detected in your area. Stay alert and monitor local weather.",
            },
            "heatwave":  {
                "title":   "🌡️ HEATWAVE ALERT",
                "message": "Extreme heat warning issued. Stay indoors between 11am–4pm. "
                           "Drink water frequently. Wear light, loose clothing. Avoid strenuous activity.",
                "safe":    "✅ No heatwave risk detected in your area. Stay hydrated and cool.",
            },
        },
        "Hindi (हिन्दी)": {
            "flag": "🇮🇳", "script": "Devanagari",
            "flood":     {
                "title":   "⚠️ बाढ़ चेतावनी",
                "message": "आपके क्षेत्र में भारी बाढ़ का खतरा है। तुरंत ऊंचे स्थान पर जाएं। "
                           "नदी किनारों और निचले इलाकों से दूर रहें। आपातकालीन किट तैयार रखें।",
                "safe":    "✅ आपके क्षेत्र में बाढ़ का कोई खतरा नहीं है। स्थानीय मौसम पर नजर रखें।",
            },
            "cyclone":   {
                "title":   "🌀 चक्रवात चेतावनी",
                "message": "आपके क्षेत्र में चक्रवात आ रहा है। घर के अंदर रहें, खिड़कियाँ बंद करें। "
                           "तटीय क्षेत्रों को तुरंत खाली करें। IMD की सूचनाएं देखें।",
                "safe":    "✅ आपके क्षेत्र में चक्रवात का कोई खतरा नहीं है।",
            },
            "landslide": {
                "title":   "⛰️ भूस्खलन चेतावनी",
                "message": "भूस्खलन का खतरा अधिक है। पहाड़ी ढलानों और कच्ची जमीन से बचें। "
                           "नदियाँ पार न करें। सुरक्षित आश्रय की ओर जाएं।",
                "safe":    "✅ आपके क्षेत्र में भूस्खलन का कोई खतरा नहीं है।",
            },
            "heatwave":  {
                "title":   "🌡️ लू / गर्मी की चेतावनी",
                "message": "अत्यधिक गर्मी की चेतावनी। दोपहर 11 से 4 बजे तक घर में रहें। "
                           "बार-बार पानी पिएं। हल्के कपड़े पहनें।",
                "safe":    "✅ आपके क्षेत्र में लू का कोई खतरा नहीं है। खूब पानी पिएं।",
            },
        },
        "Tamil (தமிழ்)": {
            "flag": "🇮🇳", "script": "Tamil",
            "flood":     {
                "title":   "⚠️ வெள்ள எச்சரிக்கை",
                "message": "உங்கள் பகுதியில் கனமழை வெள்ளம் கண்டறியப்பட்டது. உடனடியாக உயரமான இடத்திற்கு செல்லுங்கள். "
                           "ஆற்றங்கரைகள் மற்றும் தாழ்வான பகுதிகளை தவிர்க்கவும்.",
                "safe":    "✅ உங்கள் பகுதியில் வெள்ள அபாயம் இல்லை. உள்ளூர் வானிலையை கண்காணிக்கவும்.",
            },
            "cyclone":   {
                "title":   "🌀 சூறாவளி எச்சரிக்கை",
                "message": "சூறாவளி உங்கள் பகுதியை நெருங்குகிறது. வீட்டிற்குள் இருங்கள். "
                           "கடலோர பகுதிகளை உடனடியாக காலி செய்யுங்கள்.",
                "safe":    "✅ உங்கள் பகுதியில் சூறாவளி அபாயம் இல்லை.",
            },
            "landslide": {
                "title":   "⛰️ நிலச்சரிவு எச்சரிக்கை",
                "message": "நிலச்சரிவு அபாயம் அதிகமாக உள்ளது. மலை சரிவுகளை தவிர்க்கவும். "
                           "நதிகளை கடக்க வேண்டாம். பாதுகாப்பான இடத்திற்கு செல்லுங்கள்.",
                "safe":    "✅ உங்கள் பகுதியில் நிலச்சரிவு அபாயம் இல்லை.",
            },
            "heatwave":  {
                "title":   "🌡️ வெப்ப அலை எச்சரிக்கை",
                "message": "கடுமையான வெப்பம் எச்சரிக்கை. காலை 11 முதல் மாலை 4 வரை வெளியே செல்ல வேண்டாம். "
                           "அடிக்கடி தண்ணீர் குடிக்கவும்.",
                "safe":    "✅ உங்கள் பகுதியில் வெப்ப அலை அபாயம் இல்லை.",
            },
        },
        "Telugu (తెలుగు)": {
            "flag": "🇮🇳", "script": "Telugu",
            "flood":     {
                "title":   "⚠️ వరద హెచ్చరిక",
                "message": "మీ ప్రాంతంలో భారీ వరదలు గుర్తించబడ్డాయి. వెంటనే ఎత్తైన ప్రదేశానికి వెళ్ళండి. "
                           "నదీ తీరాలు మరియు నిమ్న ప్రదేశాలను నివారించండి.",
                "safe":    "✅ మీ ప్రాంతంలో వరద ముప్పు లేదు. స్థానిక వాతావరణాన్ని పర్యవేక్షించండి.",
            },
            "cyclone":   {
                "title":   "🌀 తుఫాను హెచ్చరిక",
                "message": "తుఫాను మీ ప్రాంతానికి వస్తోంది. లోపల ఉండండి. "
                           "తీర ప్రాంతాలను వెంటనే ఖాళీ చేయండి.",
                "safe":    "✅ మీ ప్రాంతంలో తుఫాను ముప్పు లేదు.",
            },
            "landslide": {
                "title":   "⛰️ భూపాతం హెచ్చరిక",
                "message": "భూపాతం ముప్పు అధికంగా ఉంది. కొండ వాలులను నివారించండి. "
                           "నదులు దాటవద్దు. సురక్షితమైన స్థలానికి వెళ్ళండి.",
                "safe":    "✅ మీ ప్రాంతంలో భూపాతం ముప్పు లేదు.",
            },
            "heatwave":  {
                "title":   "🌡️ వేడి వేవ్ హెచ్చరిక",
                "message": "తీవ్రమైన వేడి హెచ్చరిక. ఉదయం 11 నుండి సాయంత్రం 4 వరకు బయటికి వెళ్ళవద్దు. "
                           "తరచుగా నీరు త్రాగండి.",
                "safe":    "✅ మీ ప్రాంతంలో వేడి వేవ్ ముప్పు లేదు.",
            },
        },
        "Malayalam (മലയാളം)": {
            "flag": "🇮🇳", "script": "Malayalam",
            "flood":     {
                "title":   "⚠️ വെള്ളപ്പൊക്ക മുന്നറിയിപ്പ്",
                "message": "നിങ്ങളുടെ പ്രദേശത്ത് കനത്ത വെള്ളപ്പൊക്കം കണ്ടെത്തി. ഉടനടി ഉയർന്ന സ്ഥലത്തേക്ക് പോകൂ. "
                           "നദീതീരങ്ങളും താഴ്ന്ന പ്രദേശങ്ങളും ഒഴിവാക്കൂ.",
                "safe":    "✅ നിങ്ങളുടെ പ്രദേശത്ത് വെള്ളപ്പൊക്ക അപകടം ഇല്ല.",
            },
            "cyclone":   {
                "title":   "🌀 ചുഴലിക്കാറ്റ് മുന്നറിയിപ്പ്",
                "message": "ചുഴലിക്കാറ്റ് നിങ്ങളുടെ പ്രദേശത്തേക്ക് അടുക്കുന്നു. വീടിനുള്ളിൽ തുടരൂ. "
                           "തീരപ്രദേശങ്ങൾ ഉടനടി ഒഴിഞ്ഞുമാറൂ.",
                "safe":    "✅ നിങ്ങളുടെ പ്രദേശത്ത് ചുഴലിക്കാറ്റ് അപകടം ഇല്ല.",
            },
            "landslide": {
                "title":   "⛰️ മണ്ണിടിച്ചിൽ മുന്നറിയിപ്പ്",
                "message": "മണ്ണിടിച്ചിൽ അപകടം ഉയർന്നതാണ്. കുന്നിൻ ചരിവുകൾ ഒഴിവാക്കൂ. "
                           "നദികൾ കടക്കരുത്. സുരക്ഷിത സ്ഥലത്തേക്ക് പോകൂ.",
                "safe":    "✅ നിങ്ങളുടെ പ്രദേശത്ത് മണ്ണിടിച്ചിൽ അപകടം ഇല്ല.",
            },
            "heatwave":  {
                "title":   "🌡️ ചൂടലമുന്നറിയിപ്പ്",
                "message": "കടുത്ത ചൂട് മുന്നറിയിപ്പ്. രാവിലെ 11 മുതൽ വൈകുന്നേരം 4 വരെ പുറത്ത് പോകരുത്. "
                           "ധാരാളം വെള്ളം കുടിക്കൂ.",
                "safe":    "✅ നിങ്ങളുടെ പ്രദേശത്ത് ചൂടലമുന്നറിയിപ്പ് ഇല്ല.",
            },
        },
        "Kannada (ಕನ್ನಡ)": {
            "flag": "🇮🇳", "script": "Kannada",
            "flood":     {
                "title":   "⚠️ ಪ್ರವಾಹ ಎಚ್ಚರಿಕೆ",
                "message": "ನಿಮ್ಮ ಪ್ರದೇಶದಲ್ಲಿ ಭಾರಿ ಪ್ರವಾಹ ಪತ್ತೆಯಾಗಿದೆ. ತಕ್ಷಣ ಎತ್ತರದ ಸ್ಥಳಕ್ಕೆ ತೆರಳಿ. "
                           "ನದಿ ದಡಗಳು ಮತ್ತು ತಗ್ಗು ಪ್ರದೇಶಗಳನ್ನು ತಪ್ಪಿಸಿ.",
                "safe":    "✅ ನಿಮ್ಮ ಪ್ರದೇಶದಲ್ಲಿ ಪ್ರವಾಹ ಅಪಾಯ ಇಲ್ಲ.",
            },
            "cyclone":   {
                "title":   "🌀 ಚಂಡಮಾರುತ ಎಚ್ಚರಿಕೆ",
                "message": "ಚಂಡಮಾರುತ ನಿಮ್ಮ ಪ್ರದೇಶಕ್ಕೆ ಬರುತ್ತಿದೆ. ಮನೆಯಲ್ಲೇ ಇರಿ. "
                           "ಕರಾವಳಿ ಪ್ರದೇಶಗಳನ್ನು ತಕ್ಷಣ ಖಾಲಿ ಮಾಡಿ.",
                "safe":    "✅ ನಿಮ್ಮ ಪ್ರದೇಶದಲ್ಲಿ ಚಂಡಮಾರುತ ಅಪಾಯ ಇಲ್ಲ.",
            },
            "landslide": {
                "title":   "⛰️ ಭೂಕುಸಿತ ಎಚ್ಚರಿಕೆ",
                "message": "ಭೂಕುಸಿತ ಅಪಾಯ ಹೆಚ್ಚಾಗಿದೆ. ಬೆಟ್ಟದ ಇಳಿಜಾರುಗಳನ್ನು ತಪ್ಪಿಸಿ. "
                           "ನದಿಗಳನ್ನು ದಾಟಬೇಡಿ. ಸುರಕ್ಷಿತ ಸ್ಥಳಕ್ಕೆ ತೆರಳಿ.",
                "safe":    "✅ ನಿಮ್ಮ ಪ್ರದೇಶದಲ್ಲಿ ಭೂಕುಸಿತ ಅಪಾಯ ಇಲ್ಲ.",
            },
            "heatwave":  {
                "title":   "🌡️ ಶಾಖದ ಅಲೆ ಎಚ್ಚರಿಕೆ",
                "message": "ತೀವ್ರ ಶಾಖ ಎಚ್ಚರಿಕೆ. ಬೆಳಿಗ್ಗೆ 11 ರಿಂದ ಸಂಜೆ 4 ರವರೆಗೆ ಹೊರಗೆ ಹೋಗಬೇಡಿ. "
                           "ಆಗಾಗ ನೀರು ಕುಡಿಯಿರಿ.",
                "safe":    "✅ ನಿಮ್ಮ ಪ್ರದೇಶದಲ್ಲಿ ಶಾಖದ ಅಲೆ ಅಪಾಯ ಇಲ್ಲ.",
            },
        },
        "Bengali (বাংলা)": {
            "flag": "🇮🇳", "script": "Bengali",
            "flood":     {
                "title":   "⚠️ বন্যা সতর্কতা",
                "message": "আপনার এলাকায় ভারী বন্যা সনাক্ত করা হয়েছে। অবিলম্বে উঁচু জায়গায় যান। "
                           "নদীর তীর এবং নিচু এলাকা এড়িয়ে চলুন।",
                "safe":    "✅ আপনার এলাকায় কোনো বন্যার ঝুঁকি নেই। স্থানীয় আবহাওয়া পর্যবেক্ষণ করুন।",
            },
            "cyclone":   {
                "title":   "🌀 ঘূর্ণিঝড় সতর্কতা",
                "message": "ঘূর্ণিঝড় আপনার অঞ্চলের দিকে আসছে। ঘরে থাকুন। "
                           "উপকূলীয় অঞ্চল অবিলম্বে ছেড়ে যান।",
                "safe":    "✅ আপনার এলাকায় ঘূর্ণিঝড়ের ঝুঁকি নেই।",
            },
            "landslide": {
                "title":   "⛰️ ভূমিধস সতর্কতা",
                "message": "ভূমিধসের ঝুঁকি বেশি। পাহাড়ের ঢাল এড়িয়ে চলুন। "
                           "নদী পার হবেন না। নিরাপদ আশ্রয়ে যান।",
                "safe":    "✅ আপনার এলাকায় ভূমিধসের ঝুঁকি নেই।",
            },
            "heatwave":  {
                "title":   "🌡️ তাপপ্রবাহ সতর্কতা",
                "message": "তীব্র গরমের সতর্কতা। সকাল ১১টা থেকে বিকেল ৪টা পর্যন্ত বাইরে যাবেন না। "
                           "ঘন ঘন জল পান করুন।",
                "safe":    "✅ আপনার এলাকায় তাপপ্রবাহের ঝুঁকি নেই।",
            },
        },
        "Odia (ଓଡ଼ିଆ)": {
            "flag": "🇮🇳", "script": "Odia",
            "flood":     {
                "title":   "⚠️ ବନ୍ୟା ସତର୍କତା",
                "message": "ଆପଣଙ୍କ ଅଞ୍ଚଳରେ ଭାରୀ ବନ୍ୟା ଚିହ୍ନଟ ହୋଇଛି। ତୁରନ୍ତ ଉଁଚା ସ୍ଥାନକୁ ଯାଆନ୍ତୁ। "
                           "ନଦୀ କୂଳ ଏବଂ ନିମ୍ନ ଅଞ୍ଚଳ ଏଡ଼ାଇ ଚଲନ୍ତୁ।",
                "safe":    "✅ ଆପଣଙ୍କ ଅଞ୍ଚଳରେ ବନ୍ୟା ବିପଦ ନାହିଁ।",
            },
            "cyclone":   {
                "title":   "🌀 ଘୂର୍ଣ୍ଣିବାତ୍ୟା ସତର୍କତା",
                "message": "ଘୂର୍ଣ୍ଣିବାତ୍ୟା ଆପଣଙ୍କ ଅଞ୍ଚଳ ଆଡ଼କୁ ଆସୁଛି। ଘର ଭିତରେ ରୁହନ୍ତୁ। "
                           "ତଟ ଅଞ୍ଚଳ ତୁରନ୍ତ ଖାଲି କରନ୍ତୁ।",
                "safe":    "✅ ଆପଣଙ୍କ ଅଞ୍ଚଳରେ ଘୂର୍ଣ୍ଣିବାତ୍ୟା ବିପଦ ନାହିଁ।",
            },
            "landslide": {
                "title":   "⛰️ ଭୂସ୍ଖଳନ ସତର୍କତା",
                "message": "ଭୂସ୍ଖଳନ ବିପଦ ଅଧିକ। ପାହାଡ଼ ଢାଲ ଏଡ଼ାଇ ଚଲନ୍ତୁ। "
                           "ନଦୀ ପାର ହୁଅନ୍ତୁ ନାହିଁ। ସୁରକ୍ଷିତ ସ୍ଥାନକୁ ଯାଆନ୍ତୁ।",
                "safe":    "✅ ଆପଣଙ୍କ ଅଞ୍ଚଳରେ ଭୂସ୍ଖଳନ ବିପଦ ନାହିଁ।",
            },
            "heatwave":  {
                "title":   "🌡️ ତାପ ପ୍ରବାହ ସତର୍କତା",
                "message": "ତୀବ୍ର ଗରମ ସତର୍କତା। ସକାଳ ୧୧ ଠାରୁ ବିକାଳ ୪ ପର୍ଯ୍ୟନ୍ତ ବାହାରକୁ ଯାଆନ୍ତୁ ନାହିଁ। "
                           "ବାରମ୍ବାର ଜଳ ପାନ କରନ୍ତୁ।",
                "safe":    "✅ ଆପଣଙ୍କ ଅଞ୍ଚଳରେ ତାପ ପ୍ରବାହ ବିପଦ ନାହିଁ।",
            },
        },
        "Marathi (मराठी)": {
            "flag": "🇮🇳", "script": "Devanagari",
            "flood":     {
                "title":   "⚠️ पूर इशारा",
                "message": "तुमच्या परिसरात मोठा पूर आला आहे. ताबडतोब उंच ठिकाणी जा. "
                           "नदीकाठ आणि सखल भाग टाळा. आपत्कालीन किट तयार ठेवा.",
                "safe":    "✅ तुमच्या परिसरात पुराचा धोका नाही. स्थानिक हवामानावर लक्ष ठेवा.",
            },
            "cyclone":   {
                "title":   "🌀 चक्रीवादळ इशारा",
                "message": "चक्रीवादळ तुमच्या भागाकडे येत आहे. घरात राहा. "
                           "किनारपट्टी भाग ताबडतोब रिकामा करा.",
                "safe":    "✅ तुमच्या परिसरात चक्रीवादळाचा धोका नाही.",
            },
            "landslide": {
                "title":   "⛰️ भूस्खलन इशारा",
                "message": "भूस्खलनाचा धोका जास्त आहे. डोंगर उतार टाळा. "
                           "नदी ओलांडू नका. सुरक्षित ठिकाणी जा.",
                "safe":    "✅ तुमच्या परिसरात भूस्खलनाचा धोका नाही.",
            },
            "heatwave":  {
                "title":   "🌡️ उष्णतेची लाट इशारा",
                "message": "तीव्र उन्हाचा इशारा. सकाळी ११ ते दुपारी ४ वाजेपर्यंत बाहेर जाऊ नका. "
                           "वारंवार पाणी प्या.",
                "safe":    "✅ तुमच्या परिसरात उष्णतेच्या लाटेचा धोका नाही.",
            },
        },
        "Gujarati (ગુજરાતી)": {
            "flag": "🇮🇳", "script": "Gujarati",
            "flood":     {
                "title":   "⚠️ પૂર ચેતવણી",
                "message": "તમારા વિસ્તારમાં ભારે પૂર જોવા મળ્યું છે. તાત્કાલિક ઊંચી જગ્યાએ જાઓ. "
                           "નદીના કિનારા અને નીચાણવાળા વિસ્તારો ટાળો.",
                "safe":    "✅ તમારા વિસ્તારમાં પૂરનો ભય નથી. સ્થાનિક હવામાન પર નજર રાખો.",
            },
            "cyclone":   {
                "title":   "🌀 વાવાઝોડું ચેતવણી",
                "message": "વાવાઝોડું તમારા ક્ષેત્ર તરફ આવી રહ્યું છે. ઘરમાં રહો. "
                           "દરિયાકાંઠાના વિસ્તારો તાત્કાલિક ખાલી કરો.",
                "safe":    "✅ તમારા વિસ્તારમાં વાવાઝોડાનો ભય નથી.",
            },
            "landslide": {
                "title":   "⛰️ ભૂસ્ખલન ચેતવણી",
                "message": "ભૂસ્ખલનનો ભય વધારે છે. પહાડી ઢોળાવ ટાળો. "
                           "નદી ઓળંગશો નહીં. સુરક્ષિત સ્થળે જાઓ.",
                "safe":    "✅ તમારા વિસ્તારમાં ભૂસ્ખલનનો ભય નથી.",
            },
            "heatwave":  {
                "title":   "🌡️ ગરમીની લહેર ચેતવણી",
                "message": "ભારે ગરમીની ચેતવણી. સવારે ૧૧ થી સાંજે ૪ સુધી બહાર ન જાઓ. "
                           "વારંવાર પાણી પીઓ.",
                "safe":    "✅ તમારા વિસ્તારમાં ગરમીની લહેરનો ભય નથી.",
            },
        },
        "Punjabi (ਪੰਜਾਬੀ)": {
            "flag": "🇮🇳", "script": "Gurmukhi",
            "flood":     {
                "title":   "⚠️ ਹੜ੍ਹ ਚੇਤਾਵਨੀ",
                "message": "ਤੁਹਾਡੇ ਇਲਾਕੇ ਵਿੱਚ ਭਾਰੀ ਹੜ੍ਹ ਆਇਆ ਹੈ। ਤੁਰੰਤ ਉੱਚੀ ਥਾਂ ਤੇ ਜਾਓ। "
                           "ਦਰਿਆ ਦੇ ਕੰਢੇ ਅਤੇ ਨੀਵੇਂ ਇਲਾਕੇ ਤੋਂ ਦੂਰ ਰਹੋ।",
                "safe":    "✅ ਤੁਹਾਡੇ ਇਲਾਕੇ ਵਿੱਚ ਹੜ੍ਹ ਦਾ ਕੋਈ ਖ਼ਤਰਾ ਨਹੀਂ।",
            },
            "cyclone":   {
                "title":   "🌀 ਚੱਕਰਵਾਤ ਚੇਤਾਵਨੀ",
                "message": "ਚੱਕਰਵਾਤ ਤੁਹਾਡੇ ਖੇਤਰ ਵੱਲ ਆ ਰਿਹਾ ਹੈ। ਘਰ ਵਿੱਚ ਰਹੋ। "
                           "ਸਮੁੰਦਰੀ ਕੰਢੇ ਦੇ ਇਲਾਕੇ ਤੁਰੰਤ ਖਾਲੀ ਕਰੋ।",
                "safe":    "✅ ਤੁਹਾਡੇ ਇਲਾਕੇ ਵਿੱਚ ਚੱਕਰਵਾਤ ਦਾ ਕੋਈ ਖ਼ਤਰਾ ਨਹੀਂ।",
            },
            "landslide": {
                "title":   "⛰️ ਭੂਸਖਲਨ ਚੇਤਾਵਨੀ",
                "message": "ਭੂਸਖਲਨ ਦਾ ਖ਼ਤਰਾ ਵੱਧ ਹੈ। ਪਹਾੜੀ ਢਲਾਣਾਂ ਤੋਂ ਬਚੋ। "
                           "ਦਰਿਆ ਪਾਰ ਨਾ ਕਰੋ। ਸੁਰੱਖਿਅਤ ਥਾਂ ਤੇ ਜਾਓ।",
                "safe":    "✅ ਤੁਹਾਡੇ ਇਲਾਕੇ ਵਿੱਚ ਭੂਸਖਲਨ ਦਾ ਕੋਈ ਖ਼ਤਰਾ ਨਹੀਂ।",
            },
            "heatwave":  {
                "title":   "🌡️ ਗਰਮੀ ਦੀ ਲਹਿਰ ਚੇਤਾਵਨੀ",
                "message": "ਭਾਰੀ ਗਰਮੀ ਦੀ ਚੇਤਾਵਨੀ। ਸਵੇਰੇ ੧੧ ਤੋਂ ਸ਼ਾਮ ੪ ਵਜੇ ਤੱਕ ਬਾਹਰ ਨਾ ਜਾਓ। "
                           "ਵਾਰ ਵਾਰ ਪਾਣੀ ਪੀਓ।",
                "safe":    "✅ ਤੁਹਾਡੇ ਇਲਾਕੇ ਵਿੱਚ ਗਰਮੀ ਦੀ ਲਹਿਰ ਦਾ ਕੋਈ ਖ਼ਤਰਾ ਨਹੀਂ।",
            },
        },
        "Assamese (অসমীয়া)": {
            "flag": "🇮🇳", "script": "Bengali-Assamese",
            "flood":     {
                "title":   "⚠️ বানপানী সতৰ্কতা",
                "message": "আপোনাৰ অঞ্চলত ভয়াবহ বানপানী চিহ্নিত হৈছে। তৎক্ষণাৎ ওখ ঠাইলৈ যাওক। "
                           "নদীৰ পাৰ আৰু নিচু অঞ্চল পৰিহাৰ কৰক।",
                "safe":    "✅ আপোনাৰ অঞ্চলত বানপানীৰ কোনো বিপদ নাই।",
            },
            "cyclone":   {
                "title":   "🌀 ঘূৰ্ণীবতাহ সতৰ্কতা",
                "message": "ঘূৰ্ণীবতাহ আপোনাৰ অঞ্চললৈ আহিছে। ঘৰৰ ভিতৰত থাকক। "
                           "উপকূলীয় অঞ্চল তৎক্ষণাৎ খালী কৰক।",
                "safe":    "✅ আপোনাৰ অঞ্চলত ঘূৰ্ণীবতাহৰ কোনো বিপদ নাই।",
            },
            "landslide": {
                "title":   "⛰️ ভূমিস্খলন সতৰ্কতা",
                "message": "ভূমিস্খলনৰ বিপদ বেছি। পৰ্বতৰ ঢাল পৰিহাৰ কৰক। "
                           "নদী পাৰ নকৰিব। সুৰক্ষিত ঠাইলৈ যাওক।",
                "safe":    "✅ আপোনাৰ অঞ্চলত ভূমিস্খলনৰ কোনো বিপদ নাই।",
            },
            "heatwave":  {
                "title":   "🌡️ তাপ প্ৰবাহ সতৰ্কতা",
                "message": "তীব্ৰ গৰমৰ সতৰ্কতা। পুৱা ১১ৰ পৰা গধূলি ৪ বজালৈ বাহিৰত নাযাব। "
                           "সঘনাই পানী খাওক।",
                "safe":    "✅ আপোনাৰ অঞ্চলত তাপ প্ৰবাহৰ কোনো বিপদ নাই।",
            },
        },
        "Urdu (اردو)": {
            "flag": "🇮🇳", "script": "Nastaliq (RTL)",
            "flood":     {
                "title":   "⚠️ سیلاب کی وارننگ",
                "message": "آپ کے علاقے میں شدید سیلاب آیا ہے۔ فوری طور پر اونچی جگہ پر جائیں۔ "
                           "دریا کے کنارے اور نشیبی علاقوں سے دور رہیں۔",
                "safe":    "✅ آپ کے علاقے میں سیلاب کا کوئی خطرہ نہیں ہے۔",
            },
            "cyclone":   {
                "title":   "🌀 سائیکلون وارننگ",
                "message": "سائیکلون آپ کے علاقے کی طرف آ رہا ہے۔ گھر کے اندر رہیں۔ "
                           "ساحلی علاقوں کو فوری طور پر خالی کریں۔",
                "safe":    "✅ آپ کے علاقے میں سائیکلون کا کوئی خطرہ نہیں۔",
            },
            "landslide": {
                "title":   "⛰️ لینڈ سلائیڈ وارننگ",
                "message": "لینڈ سلائیڈ کا خطرہ زیادہ ہے۔ پہاڑی ڈھلوانوں سے بچیں۔ "
                           "دریا پار نہ کریں۔ محفوظ جگہ پر جائیں۔",
                "safe":    "✅ آپ کے علاقے میں لینڈ سلائیڈ کا کوئی خطرہ نہیں۔",
            },
            "heatwave":  {
                "title":   "🌡️ لو / گرمی کی لہر وارننگ",
                "message": "شدید گرمی کی وارننگ۔ صبح ۱۱ سے شام ۴ بجے تک باہر نہ جائیں۔ "
                           "بار بار پانی پیئیں۔",
                "safe":    "✅ آپ کے علاقے میں گرمی کی لہر کا کوئی خطرہ نہیں۔",
            },
        },
        "Nepali (नेपाली)": {
            "flag": "🇮🇳", "script": "Devanagari",
            "flood":     {
                "title":   "⚠️ बाढी चेतावनी",
                "message": "तपाईंको क्षेत्रमा ठूलो बाढी पत्ता लागेको छ। तुरुन्तै अग्लो ठाउँमा जानुहोस्। "
                           "नदीको किनारा र तल्लो क्षेत्र नजानुहोस्।",
                "safe":    "✅ तपाईंको क्षेत्रमा बाढीको कुनै खतरा छैन।",
            },
            "cyclone":   {
                "title":   "🌀 चक्रवात चेतावनी",
                "message": "चक्रवात तपाईंको क्षेत्रमा आउँदैछ। घरभित्र बस्नुहोस्। "
                           "तटीय क्षेत्र तुरुन्तै खाली गर्नुहोस्।",
                "safe":    "✅ तपाईंको क्षेत्रमा चक्रवातको कुनै खतरा छैन।",
            },
            "landslide": {
                "title":   "⛰️ भूस्खलन चेतावनी",
                "message": "भूस्खलनको खतरा धेरै छ। पहाडी भिरालो बाट बच्नुहोस्। "
                           "नदी नतर्नुहोस्। सुरक्षित ठाउँमा जानुहोस्।",
                "safe":    "✅ तपाईंको क्षेत्रमा भूस्खलनको कुनै खतरा छैन।",
            },
            "heatwave":  {
                "title":   "🌡️ तापलहर चेतावनी",
                "message": "अत्यधिक गर्मीको चेतावनी। बिहान ११ देखि साँझ ४ सम्म बाहिर ननिस्कनुहोस्। "
                           "बारम्बार पानी पिउनुहोस्।",
                "safe":    "✅ तपाईंको क्षेत्रमा तापलहरको कुनै खतरा छैन।",
            },
        },
        "Konkani (कोंकणी)": {
            "flag": "🇮🇳", "script": "Devanagari",
            "flood":     {
                "title":   "⚠️ पूर इशारो",
                "message": "तुमच्या परिसरांत व्हडलो पूर आयला. तत्काळ उंच जाग्यार वच. "
                           "न्हंयेचे देगे आनी सकयल्ले परिसर टाळ.",
                "safe":    "✅ तुमच्या परिसरांत पुराचो धोको ना।",
            },
            "cyclone":   {
                "title":   "🌀 चक्रीवादळ इशारो",
                "message": "चक्रीवादळ तुमच्या परिसराक येता. घरांत रव. "
                           "किनारपट्टी परिसर तत्काळ रिकामो कर.",
                "safe":    "✅ तुमच्या परिसरांत चक्रीवादळाचो धोको ना।",
            },
            "landslide": {
                "title":   "⛰️ दोंगर दरपाचो इशारो",
                "message": "दोंगर दरपाचो धोको जाद्दा आसा. दोंगराच्यो उतरणी टाळ. "
                           "न्हंय वचू नाका. सुरक्षित जाग्यार वच.",
                "safe":    "✅ तुमच्या परिसरांत दोंगर दरपाचो धोको ना।",
            },
            "heatwave":  {
                "title":   "🌡️ उश्ण लाट इशारो",
                "message": "तीव्र गर्मीचो इशारो. सकाळिं ११ थावन सांजे ४ मेरेन भायर वचू नाका. "
                           "वारेवार उदक पी.",
                "safe":    "✅ तुमच्या परिसरांत उश्ण लाटेचो धोको ना।",
            },
        },
    }

    # ── Language selector UI ─────────────────────────────────────────────────
    lang_col, hazard_col, mode_col = st.columns([2, 2, 1])
    with lang_col:
        selected_lang = st.selectbox(
            "🌐 Select Language",
            list(TRANSLATIONS.keys()),
            help="Choose any of the 16 supported languages",
        )
    with hazard_col:
        selected_hazard_lang = st.selectbox(
            "⚠️ Select Hazard Type",
            ["flood", "cyclone", "landslide", "heatwave"],
            format_func=lambda x: {
                "flood": "🌊 Flood", "cyclone": "🌀 Cyclone",
                "landslide": "⛰️ Landslide", "heatwave": "🌡️ Heatwave",
            }[x],
        )
    with mode_col:
        alert_mode = st.selectbox("🔔 Alert Mode", ["⚠️ Danger", "✅ Safe"])

    is_danger = alert_mode == "⚠️ Danger"
    t = TRANSLATIONS[selected_lang]
    h = t[selected_hazard_lang]
    msg_key = "message" if is_danger else "safe"

    hazard_color = {
        "flood": "#2980b9", "cyclone": "#e67e22",
        "landslide": "#27ae60", "heatwave": "#e74c3c",
    }[selected_hazard_lang]
    card_bg = hazard_color if is_danger else "#27ae60"

    st.markdown("---")

    # ── Alert Card Preview (Mobile-style) ────────────────────────────────────
    st.markdown('<div class="section-header">📱 Alert Preview (Mobile Style)</div>', unsafe_allow_html=True)

    is_rtl = selected_lang == "Urdu (اردو)"
    direction = "rtl" if is_rtl else "ltr"

    st.markdown(f"""
    <div style="max-width:420px;margin:0 auto;background:#1a1a2e;border-radius:20px;
                padding:1.5rem;box-shadow:0 8px 32px rgba(0,0,0,0.4);">
        <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:1rem;">
            <span style="color:#aaa;font-size:0.75rem;">HazardNet India  {t['flag']}</span>
            <span style="color:#aaa;font-size:0.75rem;">Now</span>
        </div>
        <div style="background:{card_bg};border-radius:14px;padding:1.2rem;color:white;direction:{direction};">
            <div style="font-size:1.4rem;font-weight:900;margin-bottom:0.6rem;">{h['title']}</div>
            <div style="font-size:1.0rem;line-height:1.6;opacity:0.95;">{h[msg_key]}</div>
        </div>
        <div style="margin-top:1rem;display:flex;gap:0.6rem;">
            <div style="flex:1;background:#16213e;border-radius:10px;padding:0.6rem;
                        text-align:center;color:#7ec8e3;font-size:0.8rem;font-weight:700;">
                🗺️ View Map
            </div>
            <div style="flex:1;background:#16213e;border-radius:10px;padding:0.6rem;
                        text-align:center;color:#f5a623;font-size:0.8rem;font-weight:700;">
                🚗 Evacuate
            </div>
            <div style="flex:1;background:#16213e;border-radius:10px;padding:0.6rem;
                        text-align:center;color:#7ed321;font-size:0.8rem;font-weight:700;">
                📞 SOS
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # ── All 16 Languages Alert Grid ──────────────────────────────────────────
    st.markdown('<div class="section-header">📋 All 16 Languages — Alert Message Grid</div>', unsafe_allow_html=True)
    st.caption(f"Showing **{selected_hazard_lang.title()}** alert in all supported languages")

    lang_list = list(TRANSLATIONS.items())
    for i in range(0, len(lang_list), 2):
        cols = st.columns(2)
        for j, col in enumerate(cols):
            if i + j >= len(lang_list):
                break
            lang_name, lang_data = lang_list[i + j]
            h_data = lang_data[selected_hazard_lang]
            msg_display = h_data["message"] if is_danger else h_data["safe"]
            rtl_style = "direction:rtl;text-align:right;" if lang_name == "Urdu (اردو)" else ""
            col.markdown(f"""
            <div style="background:#f8f9fa;border-radius:12px;padding:1rem;
                        margin-bottom:0.8rem;border-left:4px solid {hazard_color};">
                <div style="font-weight:800;font-size:0.95rem;color:#1e3a5f;margin-bottom:0.4rem;">
                    {lang_data['flag']} {lang_name}
                    <span style="font-size:0.7rem;color:#888;font-weight:400;margin-left:0.4rem;">
                        [{lang_data['script']}]
                    </span>
                </div>
                <div style="font-size:0.88rem;color:#333;line-height:1.5;{rtl_style}">{h_data['title']}</div>
                <div style="font-size:0.82rem;color:#555;line-height:1.55;margin-top:0.3rem;{rtl_style}">{msg_display}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")

    # ── Language Stats ────────────────────────────────────────────────────────
    st.markdown('<div class="section-header">📊 Language Coverage Stats</div>', unsafe_allow_html=True)

    lang_stats = pd.DataFrame([
        {"Language": "English",    "Script": "Latin",              "Speakers (M)": 125,  "Region": "Pan-India"},
        {"Language": "Hindi",      "Script": "Devanagari",         "Speakers (M)": 600,  "Region": "North India"},
        {"Language": "Tamil",      "Script": "Tamil",              "Speakers (M)": 80,   "Region": "Tamil Nadu"},
        {"Language": "Telugu",     "Script": "Telugu",             "Speakers (M)": 95,   "Region": "Andhra/Telangana"},
        {"Language": "Malayalam",  "Script": "Malayalam",          "Speakers (M)": 38,   "Region": "Kerala"},
        {"Language": "Kannada",    "Script": "Kannada",            "Speakers (M)": 56,   "Region": "Karnataka"},
        {"Language": "Bengali",    "Script": "Bengali",            "Speakers (M)": 100,  "Region": "West Bengal/Assam"},
        {"Language": "Odia",       "Script": "Odia",               "Speakers (M)": 38,   "Region": "Odisha"},
        {"Language": "Marathi",    "Script": "Devanagari",         "Speakers (M)": 95,   "Region": "Maharashtra"},
        {"Language": "Gujarati",   "Script": "Gujarati",           "Speakers (M)": 60,   "Region": "Gujarat"},
        {"Language": "Punjabi",    "Script": "Gurmukhi",           "Speakers (M)": 33,   "Region": "Punjab"},
        {"Language": "Assamese",   "Script": "Bengali-Assamese",   "Speakers (M)": 15,   "Region": "Assam"},
        {"Language": "Urdu",       "Script": "Nastaliq (RTL)",     "Speakers (M)": 50,   "Region": "Pan-India"},
        {"Language": "Nepali",     "Script": "Devanagari",         "Speakers (M)": 3,    "Region": "Sikkim/Darjeeling"},
        {"Language": "Konkani",    "Script": "Devanagari",         "Speakers (M)": 2.5,  "Region": "Goa/Coastal"},
    ])

    ls1, ls2 = st.columns(2)
    with ls1:
        fig_lang = px.bar(
            lang_stats.sort_values("Speakers (M)", ascending=True),
            x="Speakers (M)", y="Language", orientation="h",
            color="Speakers (M)", color_continuous_scale="Blues",
            title="Estimated Speakers per Language (Millions)",
            text="Speakers (M)",
        )
        fig_lang.update_traces(texttemplate="%{text}M", textposition="outside")
        fig_lang.update_layout(height=500, coloraxis_showscale=False)
        st.plotly_chart(fig_lang, use_container_width=True)

    with ls2:
        fig_reg = px.pie(
            lang_stats, names="Region", values="Speakers (M)",
            title="Coverage by Region",
            hole=0.4,
        )
        fig_reg.update_layout(height=500)
        st.plotly_chart(fig_reg, use_container_width=True)

    st.dataframe(lang_stats, use_container_width=True, hide_index=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 7 — DATASET
# ══════════════════════════════════════════════════════════════════════════════
with tabs[7]:
    st.markdown('<div class="section-header">📋 Dataset Explorer</div>', unsafe_allow_html=True)
    st.markdown(f"**Showing {len(df):,} records** after filters.")

    search_col = st.selectbox("Filter column", ["max_risk_label", "Land Cover", "Soil Type", "year"])
    search_val = st.selectbox("Filter value",  sorted(df[search_col].astype(str).unique()))
    filtered   = df[df[search_col].astype(str) == search_val]

    st.dataframe(
        filtered[[
            "Latitude", "Longitude", "Rainfall (mm)", "Temperature (°C)",
            "Humidity (%)", "Water Level (m)", "Elevation (m)",
            "Land Cover", "Soil Type", "max_risk_label", "year",
        ]].reset_index(drop=True),
        use_container_width=True,
        height=450,
    )

    csv_out = filtered.to_csv(index=False).encode("utf-8")
    st.download_button("⬇️ Download Filtered CSV", csv_out, "hazardnet_filtered.csv", "text/csv")

    st.markdown('<div class="section-header">📐 Dataset Statistics</div>', unsafe_allow_html=True)
    st.dataframe(df[[
        "Rainfall (mm)", "Temperature (°C)", "Humidity (%)",
        "River Discharge (m³/s)", "Water Level (m)", "Elevation (m)", "Population Density",
    ]].describe().round(2), use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 8 — ABOUT
# ══════════════════════════════════════════════════════════════════════════════
with tabs[8]:
    st.markdown('<div class="section-header">ℹ️ About HazardNet India</div>', unsafe_allow_html=True)
    st.markdown("""
**HazardNet India** is an AI-powered mobile-based disaster forecasting and early warning system designed
to predict natural disasters at a **hyperlocal level** across India.

### 🎯 Mission
Unlike existing alert systems that provide broad warnings at district or state levels, HazardNet India
focuses on **street-level risk prediction**, multilingual alerts in **15 Indian regional languages**,
and actionable evacuation guidance.

### 🌍 Disasters Covered
| Disaster | Regions |
|----------|---------|
| 🌊 Flood | Chennai, Kochi, Mumbai, Kolkata, Guwahati, Hyderabad |
| 🌀 Cyclone | Bhubaneswar, Kolkata, Chennai |
| ⛰️ Landslide | Kochi, Guwahati |
| 🌡️ Heatwave | Jaipur, Hyderabad |

### 🛠️ Technology Stack
| Layer | Technologies |
|-------|-------------|
| Frontend (Mobile) | Flutter · Dart · Google Maps API |
| Backend | FastAPI · Python |
| ML Baseline | Scikit-learn · XGBoost · Pandas |
| ML Advanced | PyTorch LSTM · TFT · Kriging · SHAP |
| Data Sources | IMD · NASA POWER · OpenWeather · NDMA |
| Database | PostgreSQL / Firebase |
| Dashboard | **Streamlit** (this app) |

### 🤖 ML Strategy
The system uses a **stacked ensemble** of three complementary models:
1. **XGBoost** — Tabular features
2. **LSTM + Attention** — 7-day rolling time-series sequences
3. **Temporal Fusion Transformer (TFT)** — Multi-horizon forecasting (1h, 6h, 12h, 24h)
4. **Kriging** — Spatial interpolation for hyperlocal GPS precision
5. **SHAP** — Explainability for every alert

### 🌐 Languages Supported
English · Hindi · Tamil · Telugu · Malayalam · Kannada · Bengali · Odia · Marathi · Gujarati · Punjabi · Assamese · Urdu · Nepali · Konkani

---
*HazardNet India — Hackathon Submission | AI-Powered Disaster Management | India*
    """)
