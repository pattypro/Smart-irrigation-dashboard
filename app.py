
import streamlit as st

st.set_page_config(page_title="Smart Irrigation Dashboard - T2", layout="centered")
st.title("🌱 Smart Irrigation Scheduler - T2 (Soil Moisture + Weather)")

st.markdown("""
This tool helps schedule irrigation based on:
- **Soil Moisture**
- **ET₀** (Reference Evapotranspiration)
- **Rain Forecast**

Based on your inputs, it calculates if irrigation is needed.
""")

with st.form("irrigation_form"):
    soil_moisture = st.number_input("Soil Moisture (% VWC)", min_value=0.0, max_value=100.0, value=60.0)
    et0 = st.number_input("ET₀ (mm/day)", min_value=0.0, value=4.5)
    rain_forecast = st.number_input("Rain Forecast (next 12 hrs, mm)", min_value=0.0, value=1.0)
    kc = st.selectbox("Crop Coefficient (Kc)", [0.45, 0.75, 1.15, 0.8], index=2)
    submit = st.form_submit_button("Run Scheduler")

if submit:
    etc = kc * et0
    st.success(f"Calculated ETc = {etc:.2f} mm/day")

    if soil_moisture < 70 and rain_forecast < 2:
        st.warning("🚿 Irrigation Recommended (T2 Condition Met)")
    else:
        st.info("✅ No Irrigation Needed Yet")
