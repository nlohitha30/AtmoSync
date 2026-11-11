
import requests

API_URL = "https://api.open-meteo.com/v1/forecast"

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
    response = requests.get(
        API_URL,
        params=params,
        timeout=20
    )

    response.raise_for_status()

    weather_data = response.json()

    print("\nAPI connection successful!")
    print("\nWeather information:")

    print("Temperature:",
          weather_data["current"]["temperature_2m"], "°C")

    print("Humidity:",
          weather_data["current"]["relative_humidity_2m"], "%")

    print("Time:",
          weather_data["current"]["time"])

except requests.exceptions.RequestException as error:
    print("API connection failed:", error)
