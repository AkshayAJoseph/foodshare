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
