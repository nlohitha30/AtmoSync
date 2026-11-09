
import requests

# Open-Meteo API URL
API_URL = "https://api.open-meteo.com/v1/forecast"

# Tirupati location coordinates
params = {
    "latitude": 13.6288,
    "longitude": 79.4192,
    "current": [
        "temperature_2m",
        "relative_humidity_2m"
    ],
    "timezone": "auto"
}

print("Connecting to Open-Meteo API...")

try:
    # Send API request
    response = requests.get(
        API_URL,
        params=params,
        timeout=20
    )

    # Check whether request was successful
    response.raise_for_status()

    # Convert response into JSON
    weather_data = response.json()

    print("\nAPI connection successful!")
    print("\nComplete API response:")
    print(weather_data)

    print("\nAPI response received successfully!")

except requests.exceptions.RequestException as error:
    print("API connection failed!")
    print("Error:", error)
