import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
import joblib

# Load dataset
df = pd.read_csv("dataset/flights.csv")
# Remove missing values
df = df.dropna(subset=['arr_delay'])

# Select features
features = [
    'arr_flights',
    'carrier_ct',
    'weather_ct',
    'nas_ct',
    'security_ct',
    'late_aircraft_ct'
]

X = df[features]
y = df['arr_delay']

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42
)

# Train model
model = RandomForestRegressor()
model.fit(X_train, y_train)

# Predictions
predictions = model.predict(X_test)

# Accuracy
mae = mean_absolute_error(y_test, predictions)

print("\n===== AI MODEL RESULTS =====")
print(f"Mean Absolute Error: {mae:.2f}")
print("\nModel successfully predicts flight delays.")


import matplotlib.pyplot as plt

importance = model.feature_importances_

feature_importance = pd.DataFrame({
    'Feature': features,
    'Importance': importance
})

feature_importance = feature_importance.sort_values(
    by='Importance',
    ascending=False
)

plt.figure(figsize=(10,6))

plt.barh(
    feature_importance['Feature'],
    feature_importance['Importance']
)
plt.title("Feature Importance")
plt.xlabel("Importance")
plt.savefig("plots/feature_importance.png")
plt.show()

joblib.dump(model, "models/delay_prediction_model.pkl")