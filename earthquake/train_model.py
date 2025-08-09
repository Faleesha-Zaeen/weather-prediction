import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import joblib

# Load earthquake data
df = pd.read_csv("earthquake_data.csv")
df['date'] = pd.to_datetime(df['date'])

# Extract date features
df['year'] = df['date'].dt.year
df['month'] = df['date'].dt.month
df['day'] = df['date'].dt.day
df['day_of_year'] = df['date'].dt.dayofyear

# Encode district/city
le_city = LabelEncoder()
df['district_encoded'] = le_city.fit_transform(df['district'])

# Features for training
X = df[['year', 'month', 'day', 'day_of_year', 'district_encoded', 'magnitude', 'depth_km', 'seismic_activity']]
y = df['earthquake']

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train RandomForest model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Save model and label encoder
joblib.dump(model, "earthquake_model.pkl")
joblib.dump(le_city, "city_encoder.pkl")

print("earthquake_model.pkl and city_encoder.pkl saved successfully!")
print(f"Test accuracy: {model.score(X_test, y_test):.3f}")
