import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# ---------------- PAGE SETTINGS ----------------
st.set_page_config(
    page_title="Agricultural Tracker Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
.main {
    background-color: #f5f7f9;
}

.stMetric {
    background-color: white;
    padding: 15px;
    border-radius: 10px;
    box-shadow: 0px 2px 6px rgba(0,0,0,0.1);
    text-align: center;
}

h1, h2, h3 {
    color: #1f4e79;
}
</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.title("🌾 Agricultural Tracker Dashboard")
st.markdown("### Water Conservation & Rain Water Harvesting System")

st.divider()

# ---------------- SIDEBAR ----------------
with st.sidebar:

    st.header("📍 Farm Details")

    farm_size = st.number_input(
        "Farm Area (sq. meters)",
        min_value=100,
        value=2000
    )

    catchment_area = st.number_input(
        "Rainwater Catchment Area (sq. meters)",
        min_value=10,
        value=500
    )

    st.header("🌧 Rainfall Data")

    rainfall_mm = st.slider(
        "Daily Rainfall (mm)",
        0,
        150,
        20
    )

    st.header("💧 Irrigation Usage")

    blue_water_liters = st.number_input(
        "Irrigation Water Used (Liters)",
        min_value=0,
        value=1500
    )

    fertilizer_kg = st.slider(
        "Fertilizer/Pesticide Used (kg)",
        0,
        100,
        10
    )

# ---------------- CALCULATIONS ----------------

# Rainwater Harvesting
harvested_water = catchment_area * rainfall_mm * 0.8

# Green Water Estimation
green_water_est = (farm_size - catchment_area) * rainfall_mm * 0.6

# Grey Water Calculation
grey_water_footprint = fertilizer_kg * 200

# ---------------- METRIC CARDS ----------------
col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "🌧 Rainwater Captured",
    f"{harvested_water:,.0f} L"
)

col2.metric(
    "🌱 Green Water",
    f"{green_water_est:,.0f} L"
)

col3.metric(
    "🚰 Blue Water",
    f"{blue_water_liters:,.0f} L"
)

col4.metric(
    "⚠ Grey Water",
    f"{grey_water_footprint:,.0f} L"
)

st.divider()

# ---------------- CHART SECTION ----------------
left_chart, right_chart = st.columns([2, 1])

# -------- BAR CHART --------
with left_chart:

    st.subheader("📊 Daily Water Spectrum Analysis")

    df = pd.DataFrame({
        "Water Type": [
            "Green Water",
            "Blue Water",
            "Grey Water"
        ],
        "Liters": [
            green_water_est,
            blue_water_liters,
            grey_water_footprint
        ],
        "Category": [
            "Natural Storage",
            "Groundwater Usage",
            "Pollution"
        ]
    })

    fig = px.bar(
        df,
        x="Water Type",
        y="Liters",
        color="Category",
        text_auto=True,
        title="Water Usage Comparison"
    )

    st.plotly_chart(fig, use_container_width=True)

# -------- STORAGE GAUGE --------
with right_chart:

    st.subheader("💧 Storage Tank Status")

    tank_capacity = 20000

    gauge = go.Figure(go.Indicator(
        mode="gauge+number",
        value=harvested_water,
        title={'text': "Water Stored Today"},
        gauge={
            'axis': {'range': [0, tank_capacity]},
            'bar': {'color': "blue"},
            'steps': [
                {'range': [0, 5000], 'color': "#ffcccc"},
                {'range': [5000, 15000], 'color': "#fff4cc"},
                {'range': [15000, 20000], 'color': "#ccffcc"}
            ]
        }
    ))

    st.plotly_chart(gauge, use_container_width=True)

# ---------------- ALERTS ----------------
st.subheader("💡 Water Conservation Recommendations")

if rainfall_mm > 10:
    st.success(
        f"High rainfall detected ({rainfall_mm} mm). "
        "Use stored rainwater and reduce groundwater pumping."
    )
else:
    st.warning(
        "Low rainfall detected. Use harvested water carefully."
    )

if grey_water_footprint > blue_water_liters:
    st.error(
        "Grey water pollution level is high. "
        "Reduce fertilizer usage and adopt organic farming methods."
    )

# ---------------- EXTRA SECTION ----------------
st.subheader("📈 System Summary")

st.write(f"""
The Agricultural Tracker system monitors:

- Rainwater harvesting capacity
- Irrigation water usage
- Soil water retention
- Pollution caused by fertilizers
- Storage tank utilization

This dashboard helps farmers improve water conservation,
reduce groundwater dependency, and support sustainable agriculture.
""")

# ---------------- FOOTER ----------------
st.divider()

st.caption(
    "BCV654A - Water Conservation and Rain Water Harvesting Project | "
    "Built using Python, Streamlit, and Plotly"
)