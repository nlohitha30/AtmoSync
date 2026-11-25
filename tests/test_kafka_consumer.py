
import unittest
from unittest.mock import patch

from kafka.structs import TopicPartition, OffsetAndMetadata

from src.kafka_consumer import (
    deserialize_sensor_message,
    create_consumer,
    commit_processed_message
)


class TestKafkaConsumer(unittest.TestCase):

    def setUp(self):
        self.valid_sensor_data = {
            "container_id": "CONT001",
            "commodity": "Rice",
            "temperature_c": 28,
            "humidity_pct": 65,
            "vibration": 0.5,
            "timestamp": "2026-11-25T09:00:00Z"
        }

    def test_valid_sensor_message_is_deserialized(self):
        message = (
            b'{"container_id":"CONT001","commodity":"Rice",'
            b'"temperature_c":28,"humidity_pct":65,'
            b'"vibration":0.5,"timestamp":"2026-11-25T09:00:00Z"}'
        )

        result = deserialize_sensor_message(message)

        self.assertEqual(result, self.valid_sensor_data)

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

    @patch("builtins.print")
    def test_missing_required_field_returns_none(self, mock_print):
        invalid_data = self.valid_sensor_data.copy()
        del invalid_data["commodity"]

        message = __import__("json").dumps(invalid_data).encode("utf-8")

        result = deserialize_sensor_message(message)

        self.assertIsNone(result)
        mock_print.assert_called_once()

    @patch("builtins.print")
    def test_invalid_humidity_returns_none(self, mock_print):
        invalid_data = self.valid_sensor_data.copy()
        invalid_data["humidity_pct"] = 150

        message = __import__("json").dumps(invalid_data).encode("utf-8")

        result = deserialize_sensor_message(message)

        self.assertIsNone(result)
        mock_print.assert_called_once()

    @patch("builtins.print")
    def test_json_list_returns_none(self, mock_print):
        message = b'["CONT001", "Rice", 28]'

        result = deserialize_sensor_message(message)

        self.assertIsNone(result)
        mock_print.assert_called_once()

    @patch("src.kafka_consumer.KafkaConsumer")
    def test_consumer_uses_manual_offset_commits(self, mock_kafka):
        create_consumer()

        mock_kafka.assert_called_once_with(
            "atmosync-sensor-data",
            bootstrap_servers=["localhost:9094"],
            auto_offset_reset="earliest",
            enable_auto_commit=False,
            group_id="atmosync-consumer-group",
            value_deserializer=deserialize_sensor_message
        )

    def test_processed_message_commits_next_offset(self):
        mock_consumer = unittest.mock.MagicMock()

        mock_message = unittest.mock.MagicMock()
        mock_message.topic = "atmosync-sensor-data"
        mock_message.partition = 0
        mock_message.offset = 10

        commit_processed_message(mock_consumer, mock_message)

        expected = {
            TopicPartition("atmosync-sensor-data", 0):
                OffsetAndMetadata(11, "")
        }

        mock_consumer.commit.assert_called_once_with(expected)


if __name__ == "__main__":
    unittest.main()
