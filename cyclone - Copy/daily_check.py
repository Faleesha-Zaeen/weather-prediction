import joblib
import pandas as pd
from datetime import datetime

# Load model and dataset
model = joblib.load("cyclone_model.pkl")
df = pd.read_csv("cyclone_data.csv")
df['date'] = pd.to_datetime(df['date'])

# Get today's date
today = datetime.today().strftime('%Y-%m-%d')
today_obj = pd.to_datetime(today)

# Check if today's date is in the dataset
row = df[df['date'] == today_obj]

if row.empty:
    result = f"[{today}]  No data available for today."
else:
    features = row[['wind_speed', 'pressure', 'humidity']]
    prediction = model.predict(features)[0]
    result = f"[{today}]  Cyclone likely today!" if prediction == 1 else f"[{today}]  No cyclone today."

# Print and log result
print(result)
with open("daily_log.txt", "a") as log_file:
    log_file.write(result + "\n")
