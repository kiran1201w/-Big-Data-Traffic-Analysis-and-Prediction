import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA
from sklearn.metrics import mean_squared_error
import requests
from io import StringIO
import math

# Step 1: Fetch Open Traffic Data
print("📥 Fetching traffic data...")
url = "https://data.cityofnewyork.us/resource/i4gi-tjb9.csv?$limit=5000"

response = requests.get(url)
if response.status_code == 200:
    print("✅ Data successfully fetched from the source.")
    traffic_data = pd.read_csv(StringIO(response.text))
else:
    print("❌ Failed to fetch data. Exiting...")
    exit()

# Step 2: Process and Clean the Data
print("🔄 Processing and cleaning the data...")
traffic_data = traffic_data[['date_time', 'volume']].dropna()
traffic_data['date_time'] = pd.to_datetime(traffic_data['date_time'])
traffic_data = traffic_data.set_index('date_time').sort_index()

# Resample the data to hourly averages
traffic_data = traffic_data.resample('H').mean().fillna(method='ffill')

# Display cleaned data
print(f"Cleaned Data:\n{traffic_data.head()}")

# Step 3: Visualize Original Traffic Data
plt.figure(figsize=(12, 6))
plt.plot(traffic_data, label='Traffic Volume', color='blue')
plt.title("Hourly Traffic Volume (NYC)")
plt.xlabel("Time")
plt.ylabel("Volume")
plt.legend()
plt.show()

# Step 4: Train-Test Split for Time Series Prediction
print("✂️ Splitting data into train and test sets...")
train_size = int(len(traffic_data) * 0.8)
train, test = traffic_data[:train_size], traffic_data[train_size:]

# Step 5: ARIMA Model for Traffic Prediction
print("🔍 Training ARIMA model...")
arima_model = ARIMA(train, order=(2, 1, 2))
arima_fit = arima_model.fit()

# Forecast using ARIMA
forecast_arima = arima_fit.forecast(steps=len(test))

# Calculate RMSE
rmse = math.sqrt(mean_squared_error(test, forecast_arima))
print(f"📊 ARIMA Model RMSE: {rmse:.2f}")

# Step 6: Visualize ARIMA Results
plt.figure(figsize=(12, 6))
plt.plot(train, label="Train Data", color='blue')
plt.plot(test, label="Actual Test Data", color='green')
plt.plot(test.index, forecast_arima, label="ARIMA Forecast", color='red')
plt.title("Traffic Volume Forecast using ARIMA")
plt.xlabel("Time")
plt.ylabel("Volume")
plt.legend()
plt.show()

print("✅ ARIMA model completed successfully!")
