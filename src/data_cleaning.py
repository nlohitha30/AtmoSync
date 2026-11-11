
import pandas as pd


def load_sensor_data(file_path):

    # Load raw sensor data
    df = pd.read_json(file_path, lines=True)

    print("RAW SENSOR DATA")
    print(df.head())

    print("\nTotal Records:", len(df))

    return df


def validate_sensor_data(df):

    print("\nDATA VALIDATION")

    # Check missing values
    print("\nMissing Values:")
    print(df.isnull().sum())

    # Check invalid humidity
    invalid_humidity = df[
        (df["humidity_pct"] < 0) |
        (df["humidity_pct"] > 100)
    ]

    print("\nInvalid Humidity Records:", len(invalid_humidity))

    # Check negative vibration
    invalid_vibration = df[df["vibration"] < 0]

    print("Invalid Vibration Records:", len(invalid_vibration))

    # Check invalid temperature values
    invalid_temperature = df[
        ~df["temperature_c"].between(-50, 100)
    ]

    print("Temperature Outside Review Range:", len(invalid_temperature))

    return df


if __name__ == "__main__":

    # Step 1: Load sensor data
    df = load_sensor_data("data/raw/sensor_data.jsonl")

    # Step 2: Validate sensor data
    df = validate_sensor_data(df)

    # Step 3: Display missing values
    print("\nMISSING VALUES")
    print(df.isnull().sum())

    # Step 4: Display data types
    print("\nDATA TYPES")
    print(df.dtypes)

import pandas as pd

df = pd.read_json("data/raw/sensor_data.jsonl", lines=True)

print("RAW SENSOR DATA")
print(df.head())

print("\nTotal Records:", len(df))


# Remove duplicate records
print("\nDUPLICATE DATA CHECK")

duplicates = df.duplicated().sum()

print("Duplicate Records:", duplicates)

df = df.drop_duplicates()

print("Records After Removing Duplicates:", len(df))

# Check missing values
print("\nMISSING VALUES CHECK")

print(df.isnull().sum())

# Remove invalid sensor readings
print("\nINVALID DATA CHECK")

df = df[
    (df["humidity_pct"].between(0, 100)) &
    (df["vibration"] >= 0) &
    (df["temperature_c"].between(-50, 100))
]

print("Records After Removing Invalid Data:", len(df))

import os

# Create processed folder if it does not exist
os.makedirs("data/processed", exist_ok=True)

# Save cleaned data
df.to_csv("data/processed/cleaned_sensor_data.csv", index=False)

print("\nCLEANING COMPLETED")
print("Cleaned data saved successfully!")
print("File: data/processed/cleaned_sensor_data.csv")