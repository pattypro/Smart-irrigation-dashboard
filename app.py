import streamlit as st
import datetime

# --- Sidebar Inputs ---
st.sidebar.title("Input Parameters")

# Select crop stage
stage = st.sidebar.selectbox("Tomato Growth Stage", ["Initial", "Vegetative", "Flowering", "Maturity"])

# Weather & sensor inputs
ET0 = st.sidebar.number_input("Reference Evapotranspiration (ET₀) [mm/day]", min_value=0.0)
forecast_rain = st.sidebar.number_input("Rain Forecast (next 6-12 hrs) [mm]", min_value=0.0)
soil_moisture = st.sidebar.slider("Soil Moisture (% Field Capacity)", 0, 100, 60)
NDVI = st.sidebar.slider("NDVI Index", 0.0, 1.0, 0.7)

# Kc values by stage
kc_values = {
    "Initial": 0.45,
    "Vegetative": 0.75,
    "Flowering": 1.15,
    "Maturity": 0.80
}

kc = kc_values[stage]
ETc = kc * ET0
net_irrigation = max(ETc - forecast_rain, 0.0)

st.title("Smart Irrigation Recommendation")
st.write(f"### Selected Stage: {stage}")
st.write(f"Kc = {kc}, ET₀ = {ET0:.2f} mm/day → ETc = {ETc:.2f} mm/day")

# Treatment-wise logic
st.subheader("Irrigation Recommendation per Treatment")

# T1: Manual
st.write("#### T1: Manual")
st.write("→ No data used. Farmer irrigates based on personal judgement.")

# T2 Logic
st.write("#### T2: Soil Moisture + Rain Forecast")
if soil_moisture < 70 and forecast_rain < 2 and stage in ["Vegetative", "Flowering"]:
    st.success("→ T2: Irrigation Recommended")
else:
    st.info("→ T2: No Irrigation Needed")

# T3 Logic
st.write("#### T3: NDVI + Rain Forecast")
ndvi_thresh = 0.7 if stage == "Vegetative" else 0.75
if NDVI < ndvi_thresh and forecast_rain < 2 and stage in ["Vegetative", "Flowering"]:
    st.success("→ T3: Irrigation Recommended")
else:
    st.info("→ T3: No Irrigation Needed")

# T4 Logic
st.write("#### T4: Integrated (ETc, Soil, NDVI, Rain)")
if (net_irrigation > 0 and soil_moisture < 80 and NDVI < 0.75 
    and stage in ["Flowering", "Vegetative"]):
    st.success(f"→ T4: Irrigation Recommended | Volume: {net_irrigation:.2f} L/m²")
else:
    st.info("→ T4: No Irrigation Needed")

# Notes
st.markdown("---")
st.caption("Note: 1 mm = 1 L/m² for your 1 m² plot.")
