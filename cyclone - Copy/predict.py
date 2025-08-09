import pandas as pd
from datetime import datetime
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import joblib

# Load data
df = pd.read_csv("cyclone_data.csv")
df['date'] = pd.to_datetime(df['date'])

# Extract date features
df['year'] = df['date'].dt.year
df['month'] = df['date'].dt.month
df['day'] = df['date'].dt.day
df['day_of_year'] = df['date'].dt.dayofyear

# Encode city/district
le_city = LabelEncoder()
df['district_encoded'] = le_city.fit_transform(df['district'])

# Features: date parts + city
X = df[['year', 'month', 'day', 'day_of_year', 'district_encoded']]
y = df['cyclone']

# Train model
model = RandomForestClassifier(random_state=42)
model.fit(X, y)

# Save model & label encoder
joblib.dump(model, "cyclone_model.pkl")
joblib.dump(le_city, "city_encoder.pkl")

def will_cyclone_on(date_str, district):
    """Predict cyclone just from date & city."""
    date_obj = pd.to_datetime(date_str)
    year = date_obj.year
    month = date_obj.month
    day = date_obj.day
    day_of_year = date_obj.timetuple().tm_yday

    # Encode city
    try:
        city_encoded = le_city.transform([district])[0]
    except ValueError:
        return None  # Unknown city

    features = [[year, month, day, day_of_year, city_encoded]]
    prediction = model.predict(features)[0]
    return bool(prediction)

def next_cyclone(city):
    """Find next cyclone date after today for given city."""
    today = datetime.now().date()
    for i in range(1, 366):  # check up to a year ahead
        future_date = today + pd.Timedelta(days=i)
        if will_cyclone_on(future_date.strftime("%Y-%m-%d"), city):
            return future_date.strftime("%Y-%m-%d")
    return None
