
# Smart Irrigation Dashboard v2

This upgraded Streamlit app allows:
- Uploading CSV files with sensor data
- Generating irrigation recommendations for T1–T4 treatments
- Visualizing uploaded sensor data

## How to Run

```bash
pip install streamlit pandas matplotlib
streamlit run app.py
```

## CSV Format Required

| ET0 | rain_mm | soil_moisture | NDVI | stage       |
|-----|---------|----------------|------|-------------|
| 4.0 | 1.5     | 65             | 0.68 | Flowering   |

The app will show recommendations and graphs based on this data.
