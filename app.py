
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("Smart Irrigation Dashboard: Per-Treatment CSV Upload")

# Upload per-treatment files
st.sidebar.header("Upload Data Per Treatment")
treatment_files = {
    "T1": st.sidebar.file_uploader("T1: Manual (Optional CSV)", type=["csv"]),
    "T2": st.sidebar.file_uploader("T2: Soil Moisture + Weather", type=["csv"]),
    "T3": st.sidebar.file_uploader("T3: NDVI + Weather", type=["csv"]),
    "T4": st.sidebar.file_uploader("T4: Integrated", type=["csv"])
}

kc_values = {
    "Initial": 0.45,
    "Vegetative": 0.75,
    "Flowering": 1.15,
    "Maturity": 0.80
}

def process_treatment(label, df):
    if df is not None:
        st.subheader(f"{label} Data Preview")
        st.dataframe(df)

        results = []
        for _, row in df.iterrows():
            stage = row["stage"]
            ET0 = float(row["ET0"])
            rain = float(row["rain_mm"])
            soil = float(row["soil_moisture"])
            ndvi = float(row["NDVI"])
            kc = kc_values.get(stage, 0.75)
            ETc = kc * ET0
            net_irrigation = max(ETc - rain, 0.0)

            if label == "T1":
                decision = "Manual"
            elif label == "T2":
                decision = "Irrigate" if soil < 70 and rain < 2 and stage in ["Vegetative", "Flowering"] else "No Irrigation"
            elif label == "T3":
                ndvi_thresh = 0.7 if stage == "Vegetative" else 0.75
                decision = "Irrigate" if ndvi < ndvi_thresh and rain < 2 and stage in ["Vegetative", "Flowering"] else "No Irrigation"
            elif label == "T4":
                decision = f"Irrigate ({net_irrigation:.2f} L/m²)" if (net_irrigation > 0 and soil < 80 and ndvi < 0.75 and stage in ["Vegetative", "Flowering"]) else "No Irrigation"
            else:
                decision = "Unknown"

            results.append({
                "stage": stage,
                "ET₀": ET0,
                "Kc": kc,
                "ETc": ETc,
                "Forecast Rain (mm)": rain,
                "Soil Moisture (%)": soil,
                "NDVI": ndvi,
                "Recommendation": decision
            })

        result_df = pd.DataFrame(results)
        st.subheader(f"{label} Recommendations")
        st.dataframe(result_df)

        # Plot available values
        st.subheader(f"{label} Sensor Data Trends")
        columns_to_plot = [col for col in ["ET0", "rain_mm", "soil_moisture", "NDVI"] if col in df.columns]
        if columns_to_plot:
            fig, ax = plt.subplots(figsize=(10, 4))
            df[columns_to_plot].plot(ax=ax, marker='o')
            plt.title(f"{label} Data Trends")
            plt.xlabel("Record Index")
            plt.grid(True)
            st.pyplot(fig)
    else:
        st.info(f"Upload CSV for {label} to see recommendations.")

# Process each treatment
for label, file in treatment_files.items():
    if file:
        df = pd.read_csv(file)
        process_treatment(label, df)
