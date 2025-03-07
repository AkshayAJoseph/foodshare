from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import pandas as pd
import joblib

orders = pd.read_csv("cleaned_orders.csv")

X = orders[["claimed_count", "days_to_expiry", "temperature"]]
y = orders["price"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = RandomForestRegressor(n_estimators=100)
model.fit(X_train, y_train)

joblib.dump(model, "pricing_model.pkl")

import numpy as np
import tensorflow as tf

# Load the trained model
model = tf.keras.models.load_model("demand_forecast.h5")

# New food item details
new_food = np.array([[5, 30]])  # Quantity available: 5, Temperature: 30°C
new_food = np.expand_dims(new_food, axis=0)

predicted_demand = model.predict(new_food)
print("Predicted Demand:", predicted_demand)

import joblib
import numpy as np

# Load pricing model
pricing_model = joblib.load("pricing_model.pkl")

# Predict price
new_item_features = np.array([[10, 3, 30]])  # 10 claims, 3 days to expiry, 30°C
recommended_price = pricing_model.predict(new_item_features.reshape(1, -1))
print("Recommended Price:", recommended_price)
