from datetime import datetime
import math


REQUIRED_FIELDS = [
    "container_id",
    "commodity",
    "temperature_c",
    "humidity_pct",
    "vibration",
    "timestamp"
]


def validate_sensor_data(data):
    errors = []

    # Check required fields
    for field in REQUIRED_FIELDS:
        if field not in data:
            errors.append(f"Missing field: {field}")

    if errors:
        return False, errors

    # Check container ID
    if not isinstance(data["container_id"], str) or not data["container_id"].strip():
        errors.append("Invalid container_id")

    # Check commodity
    if not isinstance(data["commodity"], str) or not data["commodity"].strip():
        errors.append("Invalid commodity")

    # Check temperature
    temperature = data["temperature_c"]
    if (isinstance(temperature, bool)
            or not isinstance(temperature, (int, float))
            or not math.isfinite(temperature)):
        errors.append("Temperature must be a valid number")

    # Check humidity
    humidity = data["humidity_pct"]
    if (isinstance(humidity, bool)
            or not isinstance(humidity, (int, float))
            or not math.isfinite(humidity)
            or not 0 <= humidity <= 100):
        errors.append("Humidity must be between 0 and 100")

    # Check vibration
    vibration = data["vibration"]
    if (isinstance(vibration, bool)
            or not isinstance(vibration, (int, float))
            or not math.isfinite(vibration)
            or vibration < 0):
        errors.append("Vibration must be a non-negative number")

    # Check timestamp
    try:
        datetime.fromisoformat(data["timestamp"].replace("Z", "+00:00"))
    except (ValueError, AttributeError):
        errors.append("Invalid timestamp format")

    return len(errors) == 0, errors


if __name__ == "__main__":
    sample_data = {
        "container_id": "CONT001",
        "commodity": "Avocado",
        "temperature_c": 8.5,
        "humidity_pct": 75,
        "vibration": 0.2,
        "timestamp": "2026-11-11T09:00:00Z"
    }

    is_valid, errors = validate_sensor_data(sample_data)

    if is_valid:
        print("Sensor data is VALID")
    else:
        print("Sensor data is INVALID")
        for error in errors:
            print("-", error)