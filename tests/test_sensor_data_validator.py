
import unittest

from src.iot_sensor_simulator import generate_sensor_data
from src.sensor_data_validator import validate_sensor_data


class TestSensorDataValidator(unittest.TestCase):

    def test_simulator_data_is_valid(self):
        data = generate_sensor_data()
        is_valid, errors = validate_sensor_data(data)

        self.assertTrue(is_valid)
        self.assertEqual(errors, [])

    def test_invalid_humidity_is_rejected(self):
        data = generate_sensor_data()
        data["humidity_pct"] = 150

        is_valid, errors = validate_sensor_data(data)

        self.assertFalse(is_valid)
        self.assertIn(
            "Humidity must be between 0 and 100",
            errors
        )

    def test_missing_field_is_rejected(self):
        data = generate_sensor_data()
        del data["container_id"]

        is_valid, errors = validate_sensor_data(data)

        self.assertFalse(is_valid)
        self.assertIn("Missing field: container_id", errors)


if __name__ == "__main__":
    unittest.main()
