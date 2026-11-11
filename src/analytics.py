
import pandas as pd

# Load cleaned sensor data
file_path = "data/processed/cleaned_sensor_data.csv"

df = pd.read_csv(file_path)

print("ATMoSYNC SENSOR DATA ANALYSIS")
print("=" * 40)

# 1. Total records
print("\nTotal Sensor Records:", len(df))

# 2. Container count
print("Total Containers:", df["container_id"].nunique())

# 3. Commodity count
print("Total Commodities:", df["commodity"].nunique())

# 4. Temperature analysis
print("\nTEMPERATURE ANALYSIS")
print("Average Temperature:", round(df["temperature_c"].mean(), 2))
print("Maximum Temperature:", df["temperature_c"].max())
print("Minimum Temperature:", df["temperature_c"].min())

# 5. Humidity analysis
print("\nHUMIDITY ANALYSIS")
print("Average Humidity:", round(df["humidity_pct"].mean(), 2))
print("Maximum Humidity:", df["humidity_pct"].max())
print("Minimum Humidity:", df["humidity_pct"].min())

# 6. Vibration analysis
print("\nVIBRATION ANALYSIS")
print("Average Vibration:", round(df["vibration"].mean(), 2))
print("Maximum Vibration:", df["vibration"].max())

# 7. Commodity-wise analysis
print("\nCOMMODITY-WISE ANALYSIS")
summary = df.groupby("commodity").agg({
    "temperature_c": "mean",
    "humidity_pct": "mean",
    "vibration": "mean"
}).round(2)

print(summary)

print("\nANALYSIS COMPLETED SUCCESSFULLY!")
