import pandas as pd
import joblib
from datetime import datetime


# Load the model and data
model = joblib.load("cyclone_model.pkl")
df = pd.read_csv("cyclone_data.csv")
df['date'] = pd.to_datetime(df['date'])

# Function 1: Predict for a specific date
def predict_by_date(input_date):
    try:
        date_obj = datetime.strptime(input_date, '%Y-%m-%d')
        row = df[df['date'] == date_obj]

        if row.empty:
            return f"No weather data available for {input_date}."

        features = row[['wind_speed', 'pressure', 'humidity']]
        prediction = model.predict(features)[0]

        return f" Cyclone likely on {input_date}." if prediction == 1 else f" No cyclone on {input_date}."

    except ValueError:
        return " Invalid date format. Use YYYY-MM-DD."

# Function 2: Predict all upcoming cyclone dates
def get_all_cyclone_days():
    features = df[['wind_speed', 'pressure', 'humidity']]
    predictions = model.predict(features)

    cyclone_dates = df['date'][predictions == 1]
    if cyclone_dates.empty:
        return " No cyclone days in current dataset."
    else:
        return " Cyclone likely on these dates:\n" + '\n'.join(cyclone_dates.dt.strftime('%Y-%m-%d').tolist())

# ========== USER MENU ==========
print("\n--- Cyclone Prediction System ---")
print("1. Predict for a specific date")
print("2. Show all likely cyclone dates")
choice = input("Choose option (1 or 2): ")

if choice == "1":
    date_input = input("Enter date (YYYY-MM-DD): ")
    print(predict_by_date(date_input))
elif choice == "2":
    print(get_all_cyclone_days())
else:
    print(" Invalid choice. Please choose 1 or 2.")
   

