from fastapi import FastAPI
from pydantic import BaseModel
from predict import predict_by_date, get_all_cyclone_days

app = FastAPI()

# Input format for POST requests
class DateInput(BaseModel):
    date: str  # e.g., "2025-08-01"

@app.get("/")
def read_root():
    return {"message": "🌪️ Cyclone Prediction API is running"}

@app.post("/predict/")
def predict(input: DateInput):
    result = predict_by_date(input.date)
    return {"input_date": input.date, "prediction": result}

@app.post("/cyclone-days")
def cyclone_days():
    dates = get_all_cyclone_days()
    return {"cyclone_days": dates}
