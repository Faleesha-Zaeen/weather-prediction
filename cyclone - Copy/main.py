from fastapi import FastAPI
from pydantic import BaseModel
from predict import will_cyclone_on, next_cyclone

app = FastAPI()

class DateCityInput(BaseModel):
    date: str
    city: str

class CityInput(BaseModel):
    city: str

@app.get("/")
def read_root():
    return {"message": "✅ Cyclone prediction API is working!"}

@app.post("/predict-by-date")
def predict_by_date(payload: DateCityInput):
    result = will_cyclone_on(payload.date, payload.city)
    if result is None:
        return {"error": "No data available for the given date & city"}
    return {
        "date": payload.date,
        "city": payload.city,
        "cyclone_predicted": result
    }

@app.post("/next-cyclone")
def predict_today_cyclone(payload: CityInput):
    next_date = next_cyclone(payload.city)
    if next_date is None:
        return {"city": payload.city, "message": "No upcoming cyclones found"}
    return {
        "city": payload.city,
        "next_cyclone_date": next_date
    }
