
import json
import random
import time
from datetime import datetime

# Sample container details
CONTAINERS = [
    {"container_id": "CONT001", "commodity": "Rice"},
    {"container_id": "CONT002", "commodity": "Wheat"},    {"container_id": "CONT003", "commodity": "Corn"},
    {"container_id": "CONT004", "commodity": "Coffee"}
]


def generate_sensor_data():
    container = random.choice(CONTAINERS)

    sensor_data = {
        "container_id": container["container_id"],
        "commodity": container["commodity"],
        "temperature": round(random.uniform(20, 35), 2),
        "humidity": round(random.uniform(40, 80), 2),
        "vibration": round(random.uniform(0.1, 5.0), 2),
        "timestamp": datetime.now().isoformat()
    }

    return sensor_data


if __name__ == "__main__":
    print("AtmoSync IoT Sensor Simulator Started")

    while True:
        data = generate_sensor_data()

        # Convert sensor data into JSON
        json_data = json.dumps(data, indent=4)

        print("\nGenerated Sensor Data:")
        print(json_data)

        time.sleep(2)

