
from src.data_collection import collect_weather_data

data = collect_weather_data()

for city in data:
    print(city)
