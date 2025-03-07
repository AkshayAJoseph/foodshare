import pandas as pd
import numpy as np
from datetime import timedelta

np.random.seed(42)

#enerate random dates
dates = pd.date_range(start="2025-01-01", periods=365, freq="D")

data = {
    "order_date": np.random.choice(dates, 1000),
    "food_category": np.random.choice(["Vegetables", "Fruits", "Bakery", "Dairy"], 1000),
    "quantity_available": np.random.randint(1, 20, 1000),
    "expiry_date": pd.to_datetime(np.random.choice(dates, 1000)) + timedelta(days=3),
    "claimed_count": np.random.randint(0, 20, 1000),
    "location": np.random.choice(["Area A", "Area B", "Area C"], 1000),
    "temperature": np.random.uniform(20, 40, 1000),  # simulated weather
    "price": np.random.uniform(10, 50, 1000),  # random initial pricing
}

df = pd.DataFrame(data)
df.to_csv("orders.csv", index=False)
print("Synthetic data saved!")
