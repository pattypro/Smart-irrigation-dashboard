
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("Smart Irrigation Dashboard with CSV Upload")

# File uploader for CSV
uploaded_file = st.sidebar.file_uploader("Upload Sensor Data (CSV)", type=["csv"])

if uploaded_file:
    data = pd.read_csv(uploaded_file)
    st.subheader("Uploaded Sensor Data")
    st.dataframe(data)

    # Expecting: ET0, rain_mm, soil_moisture, NDVI, stage
    kc_values = {
        "Initial": 0.45,
        "Vegetative": 0.75,
        "Flowering": 1.15,
        "Maturity": 0.80
    }

    # Add decision results
    results = []

    for _, row in data.iterrows():
        stage = row["stage"]
        ET0 = float(row["ET0"])
        rain = float(row["rain_mm"])
        soil = float(row["soil_moisture"])
        ndvi = float(row["NDVI"])
        kc = kc_values.get(stage, 0.75)
        ETc = kc * ET0
        net_irrigation = max(ETc - rain, 0.0)

        # T1
        T1 = "Manual decision by farmer"

        # T2
        T2 = "Irrigate" if soil < 70 and rain < 2 and stage in ["Vegetative", "Flowering"] else "No Irrigation"

        # T3
        ndvi_thresh = 0.7 if stage == "Vegetative" else 0.75
        T3 = "Irrigate" if ndvi < ndvi_thresh and rain < 2 and stage in ["Vegetative", "Flowering"] else "No Irrigation"

        # T4
        T4 = f"Irrigate ({net_irrigation:.2f} L/m²)" if (net_irrigation > 0 and soil < 80 and ndvi < 0.75 and stage in ["Vegetative", "Flowering"]) else "No Irrigation"

        results.append({
            "stage": stage,
            "ET₀": ET0,
            "Kc": kc,
            "ETc": ETc,
            "Forecast Rain (mm)": rain,
            "Soil Moisture (%)": soil,
            "NDVI": ndvi,
            "T1": T1,
            "T2": T2,
            "T3": T3,
            "T4": T4
        })

    result_df = pd.DataFrame(results)
    st.subheader("Irrigation Recommendations")
    st.dataframe(result_df)

    # Plot some of the uploaded variables
    st.subheader("Sensor Data Visualization")
    fig, ax = plt.subplots(figsize=(10, 4))
    data.plot(x=data.index, y=["ET0", "rain_mm", "soil_moisture", "NDVI"], ax=ax, marker='o')
    plt.title("Sensor Data Trends")
    plt.ylabel("Values")
    plt.xlabel("Record Index")
    plt.grid(True)
    st.pyplot(fig)
else:
    st.info("Please upload a CSV file with columns: ET0, rain_mm, soil_moisture, NDVI, stage")
