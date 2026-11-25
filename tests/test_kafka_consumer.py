
import unittest
from unittest.mock import patch

from src.kafka_consumer import deserialize_sensor_message


class TestKafkaConsumer(unittest.TestCase):

    def test_valid_json_message_is_deserialized(self):
        message = b'{"container_id": "CONT001", "temperature_c": 28}'

        result = deserialize_sensor_message(message)

        self.assertEqual(result["container_id"], "CONT001")
        self.assertEqual(result["temperature_c"], 28)

    @patch("builtins.print")
    def test_invalid_json_message_returns_none(self, mock_print):
        message = b'{"container_id": "CONT001"'

        result = deserialize_sensor_message(message)

        self.assertIsNone(result)
        mock_print.assert_called_once()

    @patch("builtins.print")
    def test_invalid_utf8_message_returns_none(self, mock_print):
        message = b'\xff\xfe\xfa'

        result = deserialize_sensor_message(message)

        self.assertIsNone(result)
        mock_print.assert_called_once()


if __name__ == "__main__":
    unittest.main()
