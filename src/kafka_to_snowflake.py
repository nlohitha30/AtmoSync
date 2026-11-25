
from datetime import datetime, timezone

from src.snowflake_connection import create_snowflake_connection


INSERT_QUERY = """
INSERT INTO ATMOSYNC_DB.RAW_DATA.SENSOR_DATA
(
    CONTAINER_ID,
    COMMODITY,
    TEMPERATURE_C,
    HUMIDITY_PCT,
    VIBRATION,
    TIMESTAMP
)
VALUES (%s, %s, %s, %s, %s, %s)
"""


def insert_sensor_data(sensor_data):
    """
    Insert one validated Kafka sensor record into Snowflake.
    """

    required_fields = [
        "container_id",
        "commodity",
        "temperature_c",
        "humidity_pct",
        "vibration",
        "timestamp"
    ]

    if not isinstance(sensor_data, dict):
        raise ValueError("Sensor data must be a dictionary.")

    missing_fields = [
        field for field in required_fields
        if field not in sensor_data
    ]

    if missing_fields:
        raise ValueError(
            f"Missing sensor fields: {missing_fields}"
        )

    timestamp_value = sensor_data["timestamp"]

    if isinstance(timestamp_value, str):
        timestamp_value = datetime.fromisoformat(
            timestamp_value.replace("Z", "+00:00")
        )

    if timestamp_value.tzinfo is not None:
        timestamp_value = timestamp_value.astimezone(
            timezone.utc
        ).replace(tzinfo=None)

    values = (
        sensor_data["container_id"],
        sensor_data["commodity"],
        float(sensor_data["temperature_c"]),
        float(sensor_data["humidity_pct"]),
        float(sensor_data["vibration"]),
        timestamp_value
    )

    conn = create_snowflake_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(INSERT_QUERY, values)
        conn.commit()

        print(
            f"Sensor record inserted successfully: "
            f"{sensor_data['container_id']}"
        )

        return True

    except Exception:
        conn.rollback()
        raise

    finally:
        cursor.close()
        conn.close()
