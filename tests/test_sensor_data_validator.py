
import pytest
from src.sensor_data_validator import validate_sensor_data


def get_valid_sensor_data():
    return {
        "container_id": "CONT001",
        "commodity": "Avocado",
        "temperature_c": 8.5,
        "humidity_pct": 75,
        "vibration": 0.2,
        "timestamp": "2026-11-14T09:00:00Z"
    }


def test_valid_sensor_data():
    data = get_valid_sensor_data()

    is_valid, errors = validate_sensor_data(data)

    assert is_valid is True
    assert errors == []


def test_missing_required_field():
    data = get_valid_sensor_data()
    del data["commodity"]

    is_valid, errors = validate_sensor_data(data)

    assert is_valid is False
    assert "Missing field: commodity" in errors


@pytest.mark.parametrize("humidity", [-10, 101])
def test_invalid_humidity(humidity):
    data = get_valid_sensor_data()
    data["humidity_pct"] = humidity

    is_valid, errors = validate_sensor_data(data)

    assert is_valid is False
    assert "Humidity must be between 0 and 100" in errors


def test_negative_vibration():
    data = get_valid_sensor_data()
    data["vibration"] = -2

    is_valid, errors = validate_sensor_data(data)

    assert is_valid is False
    assert "Vibration must be a non-negative number" in errors