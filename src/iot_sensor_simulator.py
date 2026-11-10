
import json
import random
import time
from datetime import datetime, timezone

CONTAINERS = [
    {"container_id": "CONT001", "commodity": "Rice"},
    {"container_id": "CONT002", "commodity": "Wheat"},
    {"container_id": "CONT003", "commodity": "Corn"},
    {"container_id": "CONT004", "commodity": "Coffee"}
]

def generate_sensor_data():
    container = random.choice(CONTAINERS)

    sensor_data = {
        "container_id": container["container_id"],
        "commodity": container["commodity"],
        "temperature_c": round(random.uniform(20, 35), 2),
        "humidity_pct": round(random.uniform(40, 80), 2),
        "vibration": round(random.uniform(0.1, 5.0), 2),
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

    return sensor_data


if __name__ == "__main__":
    print("AtmoSync IoT Sensor Simulator Started")

    while True:
        data = generate_sensor_data()
        print(json.dumps(data, indent=4))
        time.sleep(2)
