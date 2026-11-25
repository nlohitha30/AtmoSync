
import unittest
from unittest.mock import MagicMock, patch

from src.kafka_to_snowflake import insert_sensor_data


class TestKafkaToSnowflake(unittest.TestCase):

    def setUp(self):
        self.sensor_data = {
            "container_id": "CONT001",
            "commodity": "Rice",
            "temperature_c": 28,
            "humidity_pct": 65,
            "vibration": 0.5,
            "timestamp": "2026-11-25T09:00:00Z"
        }

    @patch("src.kafka_to_snowflake.create_snowflake_connection")
    def test_valid_sensor_data_is_inserted(self, mock_connection):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()

        mock_connection.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        result = insert_sensor_data(self.sensor_data)

        self.assertTrue(result)
        mock_cursor.execute.assert_called_once()
        mock_conn.commit.assert_called_once()
        mock_cursor.close.assert_called_once()
        mock_conn.close.assert_called_once()

    @patch("src.kafka_to_snowflake.create_snowflake_connection")
    def test_database_error_rolls_back(self, mock_connection):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()

        mock_connection.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.execute.side_effect = Exception("Database error")

        with self.assertRaises(Exception):
            insert_sensor_data(self.sensor_data)

        mock_conn.rollback.assert_called_once()
        mock_conn.close.assert_called_once()

    @patch("src.kafka_to_snowflake.create_snowflake_connection")
    def test_missing_field_is_rejected(self, mock_connection):
        invalid_data = self.sensor_data.copy()
        del invalid_data["commodity"]

        with self.assertRaises(ValueError):
            insert_sensor_data(invalid_data)

        mock_connection.assert_not_called()


if __name__ == "__main__":
    unittest.main()
