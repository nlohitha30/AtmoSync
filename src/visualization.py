
import pandas as pd
import matplotlib.pyplot as plt
import os

# Load cleaned sensor data
df = pd.read_csv("data/processed/cleaned_sensor_data.csv")

# Create charts folder
os.makedirs("static/charts", exist_ok=True)

# 1. Temperature chart
plt.figure(figsize=(8, 5))
temperature = df.groupby("commodity")["temperature_c"].mean()
temperature.plot(kind="bar")
plt.title("Average Temperature by Commodity")
plt.xlabel("Commodity")
plt.ylabel("Temperature (°C)")
plt.tight_layout()
plt.savefig("static/charts/temperature_chart.png")
plt.close()

# 2. Humidity chart
plt.figure(figsize=(8, 5))
humidity = df.groupby("commodity")["humidity_pct"].mean()
humidity.plot(kind="bar")
plt.title("Average Humidity by Commodity")
plt.xlabel("Commodity")
plt.ylabel("Humidity (%)")
plt.tight_layout()
plt.savefig("static/charts/humidity_chart.png")
plt.close()

# 3. Vibration chart
plt.figure(figsize=(8, 5))
vibration = df.groupby("commodity")["vibration"].mean()
vibration.plot(kind="bar")
plt.title("Average Vibration by Commodity")
plt.xlabel("Commodity")
plt.ylabel("Vibration")
plt.tight_layout()
plt.savefig("static/charts/vibration_chart.png")
plt.close()

print("All 3 charts generated successfully!")
print("Charts saved in static/charts/")
