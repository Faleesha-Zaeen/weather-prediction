from fastapi import FastAPI
from pydantic import BaseModel
from .predict import will_earthquake_on, next_earthquake


app = FastAPI()

class DateCityInput(BaseModel):
    date: str
    city: str

class CityInput(BaseModel):
    city: str

@app.get("/")
def read_root():
    return {"message": "✅ Earthquake prediction API is working!"}

@app.post("/predict-by-date")
def predict_by_date(payload: DateCityInput):
    result = will_earthquake_on(payload.date, payload.city)
    if result is None:
        return {"error": "No data available for the given date & city"}
    return {
        "date": payload.date,
        "city": payload.city,
        "earthquake_predicted": result
    }

@app.post("/next-earthquake")
def predict_next_earthquake(payload: CityInput):
    next_date = next_earthquake(payload.city)
    if next_date is None:
        return {"city": payload.city, "message": "No upcoming earthquakes found"}
    return {
        "city": payload.city,
        "next_earthquake_date": next_date
    }
