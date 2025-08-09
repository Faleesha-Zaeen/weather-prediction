import streamlit as st
import pandas as pd
import joblib
from datetime import datetime

# Load model and data
model = joblib.load("cyclone_model.pkl")
df = pd.read_csv("cyclone_data.csv")
df['date'] = pd.to_datetime(df['date'])

st.title(" Cyclone Prediction System")

# Option 1: Predict for specific date
st.subheader(" Check cyclone on a specific date")
date_input = st.date_input("Enter a date")

if st.button("Predict"):
    row = df[df['date'] == pd.to_datetime(date_input)]
    if row.empty:
        st.warning("No data available for this date.")
    else:
        features = row[['wind_speed', 'pressure', 'humidity']]
        prediction = model.predict(features)[0]
        if prediction == 1:
            st.error(f" Cyclone likely on {date_input}")
        else:
            st.success(f" No cyclone on {date_input}")

# Option 2: Show all upcoming cyclone dates
st.subheader(" Show all likely cyclone dates")

if st.button("Show All"):
    features = df[['wind_speed', 'pressure', 'humidity']]
    predictions = model.predict(features)
    cyclone_dates = df['date'][predictions == 1]
    if cyclone_dates.empty:
        st.info("No cyclone dates in dataset.")
    else:
        st.write(" Cyclone predicted on:")
        st.write(cyclone_dates.dt.strftime('%Y-%m-%d').tolist())

        
