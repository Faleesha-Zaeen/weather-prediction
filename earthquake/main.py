from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import pandas as pd
from datetime import datetime, date

app = FastAPI()

# Load earthquake model and dataset
model = joblib.load("earthquake_model.pkl")
df = pd.read_csv("earthquake_data.csv")
df['date'] = pd.to_datetime(df['date'])

# Input schema for POST
class DateInput(BaseModel):
    date: str  # e.g. "2025-08-04"

# Root route
@app.get("/")
def read_root():
    return {"message": "✅ Earthquake prediction API is working!"}

# POST endpoint for prediction
@app.post("/predict/")
def predict_earthquake(input: DateInput):
    try:
        date_obj = datetime.strptime(input.date, "%Y-%m-%d")
        row = df[df['date'] == date_obj]

        if row.empty:
            return {"result": f"❌ No data available for {input.date}"}

        features = row[['magnitude', 'depth_km', 'seismic_activity']]
        prediction = model.predict(features)[0]

        if prediction == 1:
            return {"result": f"🌍 Earthquake likely on {input.date}"}
        else:
            return {"result": f"✅ No earthquake on {input.date}"}
    except KeyError as e:
        raise HTTPException(status_code=400, detail=f"Missing column in dataset: {e}")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# GET endpoint with query param
@app.get("/predict-by-date/")
def predict_by_date(date: str):
    try:
        date_obj = datetime.strptime(date, "%Y-%m-%d")
        row = df[df['date'] == date_obj]

        if row.empty:
            return {"result": f"❌ No data available for {date}"}

        features = row[['magnitude', 'depth_km', 'seismic_activity']]
        prediction = model.predict(features)[0]

        if prediction == 1:
            return {"result": f"🌍 Earthquake likely on {date}"}
        else:
            return {"result": f"✅ No earthquake on {date}"}
    except ValueError:
        raise HTTPException(status_code=400, detail="❌ Invalid date format. Use YYYY-MM-DD.")
    except KeyError as e:
        raise HTTPException(status_code=400, detail=f"Missing column in dataset: {e}")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# GET endpoint to view all predicted earthquake dates
@app.get("/earthquake-dates/")
def get_all_earthquake_dates():
    try:
        features = df[['magnitude', 'depth_km', 'seismic_activity']]
        predictions = model.predict(features)
        earthquake_dates = df['date'][predictions == 1]

        if earthquake_dates.empty:
            return {"earthquake_dates": []}
        return {"earthquake_dates": earthquake_dates.dt.strftime('%Y-%m-%d').tolist()}
    except KeyError as e:
        raise HTTPException(status_code=400, detail=f"Missing column in dataset: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# GET endpoint to check earthquake prediction for today
@app.get("/today-earthquake/")
def predict_today_earthquake():
    try:
        today = pd.to_datetime(date.today())
        row = df[df['date'] == today]

        if row.empty:
            return {"result": f"❌ No data available for today ({today.date()})"}

        features = row[['magnitude', 'depth_km', 'seismic_activity']]
        prediction = model.predict(features)[0]

        if prediction == 1:
            return {"result": f"🌍 Earthquake likely today ({today.date()})"}
        else:
            return {"result": f"✅ No earthquake today ({today.date()})"}
    except KeyError as e:
        raise HTTPException(status_code=400, detail=f"Missing column in dataset: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
