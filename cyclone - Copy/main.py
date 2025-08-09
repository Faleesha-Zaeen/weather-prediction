from fastapi import FastAPI, HTTPException 
from pydantic import BaseModel
import joblib
import pandas as pd
from datetime import datetime, date

app = FastAPI()

# Load model and dataset
model = joblib.load("cyclone_model.pkl")
df = pd.read_csv("cyclone_data.csv")
df['date'] = pd.to_datetime(df['date'])

# Input schema for POST
class DateInput(BaseModel):
    date: str  # e.g. "2025-08-04"

# Root route
@app.get("/")
def read_root():
    return {"message": "✅ Cyclone prediction API is working!"}

# POST endpoint for tools (Swagger, Postman)
@app.post("/predict/")
def predict_cyclone(input: DateInput):
    try:
        date_obj = datetime.strptime(input.date, "%Y-%m-%d")
        row = df[df['date'] == date_obj]

        if row.empty:
            return {"result": f"❌ No data available for {input.date}"}

        features = row[['wind_speed', 'pressure', 'humidity']]
        prediction = model.predict(features)[0]

        if prediction == 1:
            return {"result": f"🌪 Cyclone likely on {input.date}"}
        else:
            return {"result": f"✅ No cyclone on {input.date}"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# ✅ GET endpoint for browser (with URL query)
@app.get("/predict-by-date/")
def predict_by_date(date: str):
    try:
        date_obj = datetime.strptime(date, "%Y-%m-%d")
        row = df[df['date'] == date_obj]

        if row.empty:
            return {"result": f"❌ No data available for {date}"}

        features = row[['wind_speed', 'pressure', 'humidity']]
        prediction = model.predict(features)[0]

        if prediction == 1:
            return {"result": f"🌪 Cyclone likely on {date}"}
        else:
            return {"result": f"✅ No cyclone on {date}"}
    except ValueError:
        raise HTTPException(status_code=400, detail="❌ Invalid date format. Use YYYY-MM-DD.")

# ✅ GET endpoint to view all cyclone dates
@app.get("/cyclone-dates/")
def get_all_cyclone_dates():
    features = df[['wind_speed', 'pressure', 'humidity']]
    predictions = model.predict(features)
    cyclone_dates = df['date'][predictions == 1]

    if cyclone_dates.empty:
        return {"cyclone_dates": []}
    return {"cyclone_dates": cyclone_dates.dt.strftime('%Y-%m-%d').tolist()}

# ✅ NEW FUNCTION: Check for cyclone today
@app.get("/today-cyclone/")
def predict_today_cyclone():
    today = pd.to_datetime(date.today())
    row = df[df['date'] == today]

    if row.empty:
        return {"result": f"❌ No data available for today ({today.date()})"}

    features = row[['wind_speed', 'pressure', 'humidity']]
    prediction = model.predict(features)[0]

    if prediction == 1:
        return {"result": f"🌪 Cyclone likely today ({today.date()})"}
    else:
        return {"result": f"✅ No cyclone today ({today.date()})"}