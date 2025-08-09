import pandas as pd
import joblib
from sklearn.ensemble import RandomForestClassifier

# Load dataset
df = pd.read_csv("cyclone_data.csv")
df['date'] = pd.to_datetime(df['date'])

# Train model
X = df[['wind_speed', 'pressure', 'humidity']]
y = df['cyclone']
model = RandomForestClassifier(random_state=42)
model.fit(X, y)

# Save model
joblib.dump(model, "cyclone_model.pkl")
print("✅ Model saved as cyclone_model.pkl")
