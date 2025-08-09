# train_model.py
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import joblib

df = pd.read_csv("earthquake_data.csv")

X = df[['magnitude', 'depth_km', 'seismic_activity']]
y = df['earthquake']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

joblib.dump(model, "earthquake_model.pkl")
print(" earthquake_model.pkl saved")
print(f"Test accuracy: {model.score(X_test, y_test):.3f}")
