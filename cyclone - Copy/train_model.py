import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import classification_report
import joblib  # To save the trained model

# Load dataset
df = pd.read_csv("cyclone_data.csv")

# Features and target
X = df[['wind_speed', 'pressure', 'humidity']]
y = df['cyclone']

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Model
model = DecisionTreeClassifier()
model.fit(X_train, y_train)

# Evaluation
y_pred = model.predict(X_test)
print(" Model Evaluation Report:\n")
print(classification_report(y_test, y_pred))

# Save the model
joblib.dump(model, 'cyclone_model.pkl')
print(" Model trained and saved as 'cyclone_model.pkl'")
