# predict.py
import pandas as pd
import joblib
from datetime import datetime

model = joblib.load("earthquake_model.pkl")
df = pd.read_csv("earthquake_data.csv")
df['date'] = pd.to_datetime(df['date'])

def check(date_str, district=None):
    d = datetime.strptime(date_str, "%Y-%m-%d")
    data = df[df['date'] == d]
    if district:
        data = data[data['district'].str.lower() == district.lower()]
    if data.empty:
        return f"No data for {district or 'any district'} on {date_str}"
    pred = model.predict(data[['magnitude', 'depth_km', 'seismic_activity']])[0]
    return " Earthquake likely" if pred == 1 else " No earthquake"

print(check("2025-01-01", "Chennai"))
