import os
import pandas as pd
from datetime import datetime, timedelta
import joblib

# Get folder path of this file (predict.py)
base_dir = os.path.dirname(__file__)

# Load saved model and label encoder using relative paths
model = joblib.load(os.path.join(base_dir, "earthquake_model.pkl"))
le_city = joblib.load(os.path.join(base_dir, "city_encoder.pkl"))

# Load full data for reference and features
df = pd.read_csv(os.path.join(base_dir, "earthquake_data.csv"))
df['date'] = pd.to_datetime(df['date'])

# Extract date features in dataframe for reference
df['year'] = df['date'].dt.year
df['month'] = df['date'].dt.month
df['day'] = df['date'].dt.day
df['day_of_year'] = df['date'].dt.dayofyear

# Encode district names in dataframe for filtering
df['district_encoded'] = le_city.transform(df['district'])

def will_earthquake_on(date_str, district):
    """Return True/False if earthquake predicted, None if unknown city or no data."""
    try:
        date_obj = pd.to_datetime(date_str)
    except Exception:
        return None

    try:
        city_encoded = le_city.transform([district])[0]
    except ValueError:
        return None  # Unknown district/city

    # Filter data for this date & city
    data = df[(df['date'] == date_obj) & (df['district_encoded'] == city_encoded)]
    if data.empty:
        return None

    # Prepare features in the exact order as training
    features = data[['year', 'month', 'day', 'day_of_year', 'district_encoded', 'magnitude', 'depth_km', 'seismic_activity']]

    prediction = model.predict(features)[0]
    return bool(prediction)

def next_earthquake(district):
    """Return the next date (string) where earthquake is predicted for district, or None."""
    try:
        city_encoded = le_city.transform([district])[0]
    except ValueError:
        return None

    today = datetime.now().date()

    # Check each day up to 365 days in the future
    for i in range(1, 366):
        future_date = today + timedelta(days=i)
        if will_earthquake_on(future_date.strftime("%Y-%m-%d"), district):
            return future_date.strftime("%Y-%m-%d")

    return None
