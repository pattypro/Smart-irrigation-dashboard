
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("Smart Irrigation Dashboard: Per-Treatment Decision Support")

# Upload per-treatment files
st.sidebar.header("Upload Data Per Treatment")
treatment_files = {
    "T1": st.sidebar.file_uploader("T1: Manual (Optional CSV)", type=["csv"]),
    "T2": st.sidebar.file_uploader("T2: Soil Moisture + Rain Forecast", type=["csv"]),
    "T3": st.sidebar.file_uploader("T3: NDVI + Rain Forecast", type=["csv"]),
    "T4": st.sidebar.file_uploader("T4: Integrated Smart Logic", type=["csv"])
}

kc_values = {
    "Initial": 0.45,
    "Vegetative": 0.75,
    "Flowering": 1.15,
    "Fruiting": 1.05,
    "Maturity": 0.80
}

def process_treatment(label, df):
    if df is not None:
        st.subheader(f"{label} Data Preview")
        st.dataframe(df)

        results = []
        for _, row in df.iterrows():
            stage = row.get("stage", "Vegetative")
            ET0 = float(row.get("ET0", 0.0))
            rain = float(row.get("rain_mm", 0.0))
            soil = float(row.get("soil_moisture", 100))
            ndvi = float(row.get("NDVI", 0.8))  # Optional
            kc = kc_values.get(stage, 0.75)
            ETc = kc * ET0
            net_irrigation = max(ETc - rain, 0.0)

            # T1: No automation
            if label == "T1":
                decision = "Manual – Farmer determines irrigation"
                volume = "-"

            # T2 Logic: Soil + Rain + Stage (active growth)
            elif label == "T2":
                if soil < 70 and rain < 2 and stage in ["Vegetative", "Flowering", "Fruiting"]:
                    decision = "Irrigate"
                    volume = f"{net_irrigation:.2f} L/m²"
                else:
                    decision = "No Irrigation"
                    volume = "0.00 L/m²"

            # T3 Logic: NDVI + Rain + Stage
            elif label == "T3":
                ndvi_thresh = 0.7 if stage == "Vegetative" else 0.75
                if ndvi < ndvi_thresh and rain < 2 and stage in ["Vegetative", "Flowering", "Fruiting"]:
                    decision = "Irrigate"
                    volume = f"{net_irrigation:.2f} L/m²"
                else:
                    decision = "No Irrigation"
                    volume = "0.00 L/m²"

            # T4 Logic: ETc > Rain + Soil + NDVI + Stage (flowering/fruition only)
            elif label == "T4":
                if net_irrigation > 0 and soil < 80 and ndvi < 0.75 and stage in ["Flowering", "Fruiting"]:
                    decision = "Irrigate"
                    volume = f"{net_irrigation:.2f} L/m²"
                else:
                    decision = "No Irrigation"
                    volume = "0.00 L/m²"
            else:
                decision = "Unknown"
                volume = "-"

            results.append({
                "stage": stage,
                "ET₀": ET0,
                "Kc": kc,
                "ETc": ETc,
                "Rain Forecast (mm)": rain,
                "Soil Moisture (%)": soil,
                "NDVI": ndvi if "NDVI" in df.columns else "N/A",
                "Recommendation": decision,
                "Predicted Volume": volume
            })

        result_df = pd.DataFrame(results)
        st.subheader(f"{label} Daily Irrigation Recommendation")
        st.dataframe(result_df)

        # Plot if data available
        st.subheader(f"{label} Sensor Data Trend")
        cols = [col for col in ["ET0", "rain_mm", "soil_moisture", "NDVI"] if col in df.columns]
        if cols:
            fig, ax = plt.subplots(figsize=(10, 4))
            df[cols].plot(ax=ax, marker='o')
            plt.title(f"{label} Data Trends")
            plt.xlabel("Sample Index")
            plt.grid(True)
            st.pyplot(fig)
    else:
        st.info(f"Upload a CSV for {label} to process irrigation decisions.")

# Run for each treatment
for label, file in treatment_files.items():
    if file:
        df = pd.read_csv(file)
        process_treatment(label, df)
