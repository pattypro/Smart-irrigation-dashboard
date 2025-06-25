# Smart Irrigation Dashboard

This Streamlit app provides smart irrigation scheduling for tomato plots using real-time sensor data (soil moisture, NDVI) and weather data (ET₀ and short-term rain forecast). It supports four irrigation strategies (T1–T4) with increasing levels of data-driven logic.

## Features

- Manual and sensor-based irrigation decision logic
- Integrated ETc calculation using crop coefficients (Kc)
- NDVI-based vegetative stress assessment
- Rain forecast logic for optimizing irrigation
- Simple input sliders and recommendations per treatment

## Requirements

- Python 3.7+
- Streamlit

## Run Locally

```bash
pip install streamlit
streamlit run app.py
```

## Notes

- 1 mm = 1 L/m² for your 1 m² tomato plots.
- Kc values are adapted from FAO56 recommendations.
