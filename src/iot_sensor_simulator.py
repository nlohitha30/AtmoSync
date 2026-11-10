
import random
import time
from datetime import datetime

def generate_sensor_data():

    data = {
        "container_id": "CONTAINER_01",
        "timestamp": datetime.now().isoformat(),
        "temperature": round(random.uniform(20, 40), 2),
        "humidity": round(random.uniform(40, 90), 2),
        "vibration": round(random.uniform(0.1, 5.0), 2)
    }

    return data


if __name__ == "__main__":

    print("AtmoSync IoT Sensor Simulator Started")

    while True:
        
        sensor_data = generate_sensor_data()

        print(sensor_data)

        time.sleep(2)