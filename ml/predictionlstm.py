import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
import numpy as np

orders = pd.read_csv("cleaned_orders.csv")

X = []
y = []
time_steps = 5  

for i in range(len(orders) - time_steps):
    X.append(orders.iloc[i:i+time_steps][["quantity_available", "temperature"]].values)
    y.append(orders.iloc[i+time_steps]["claimed_count"])

X = np.array(X)
y = np.array(y)

split = int(0.8 * len(X))
X_train, X_test, y_train, y_test = X[:split], X[split:], y[:split], y[split:]

model = Sequential([
    LSTM(50, activation='relu', return_sequences=True, input_shape=(time_steps, 2)),
    LSTM(50, activation='relu'),
    Dense(1)
])

model.compile(optimizer='adam', loss='mse')
model.fit(X_train, y_train, epochs=20, batch_size=8, validation_data=(X_test, y_test))

model.save("demand_forecast.h5")
