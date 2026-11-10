
import requests

CITIES = {
    "Tirupati": (13.6288, 79.4192),
    "Bengaluru": (12.9716, 77.5946),
    "Chennai": (13.0827, 80.2707),
    "Hyderabad": (17.3850, 78.4867)
}

def collect_weather_data():

    weather_data = []

    for city, coordinates in CITIES.items():

        latitude, longitude = coordinates

        url = "https://api.open-meteo.com/v1/forecast"

        params = {
            "latitude": latitude,
            "longitude": longitude,
            "current": "temperature_2m,relative_humidity_2m,precipitation,wind_speed_10m"
        }

        response = requests.get(url, params=params)
        response.raise_for_status()

        data = response.json()
        current = data["current"]

        weather_data.append({
            "City": city,
            "Temperature": current["temperature_2m"],
            "Humidity": current["relative_humidity_2m"],
            "Rainfall": current["precipitation"],
            "Wind Speed": current["wind_speed_10m"]
        })

    return weather_data
