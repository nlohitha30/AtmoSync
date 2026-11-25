
import os
import json

from kafka import KafkaConsumer, TopicPartition
from kafka.structs import OffsetAndMetadata

from src.sensor_data_validator import validate_sensor_data
from src.kafka_to_snowflake import insert_sensor_data


KAFKA_SERVER = os.getenv("KAFKA_SERVER", "localhost:9094")
KAFKA_TOPIC = "atmosync-sensor-data"


def deserialize_sensor_message(message):
    """Deserialize and validate a Kafka sensor message."""

    try:
        data = json.loads(message.decode("utf-8"))

    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        print(f"Rejected invalid Kafka message: {error}")
        return None

    if not isinstance(data, dict):
        print("Rejected Kafka message: Expected a JSON object.")
        return None

    is_valid, errors = validate_sensor_data(data)

    if not is_valid:
        print(f"Rejected invalid sensor data: {errors}")
        return None

    return data


def create_consumer():
    """Create Kafka consumer with manual offset commits."""

    consumer = KafkaConsumer(
        KAFKA_TOPIC,
        bootstrap_servers=[KAFKA_SERVER],
        auto_offset_reset="earliest",
        enable_auto_commit=False,
        group_id="atmosync-consumer-group",
        value_deserializer=deserialize_sensor_message
    )

    return consumer


def commit_processed_message(consumer, message):
    """Commit only the offset of the processed Kafka message."""

    topic_partition = TopicPartition(
        message.topic,
        message.partition
    )

    next_offset = OffsetAndMetadata(
        message.offset + 1,
        ""
    )

    consumer.commit({
        topic_partition: next_offset
    })


if __name__ == "__main__":
    print("AtmoSync Kafka Consumer Started")
    print("Kafka to Snowflake integration enabled")

    consumer = create_consumer()

    try:
        for message in consumer:

            # Invalid messages are deliberately rejected.
            if message.value is None:
                commit_processed_message(consumer, message)
                continue

            print("\nValid Sensor Data Received:")
            print(json.dumps(message.value, indent=4))

            try:
                # Save the validated record into Snowflake.
                insert_sensor_data(message.value)

                # Commit only after successful database insertion.
                commit_processed_message(consumer, message)

                print("Kafka message successfully processed.")

            except Exception as error:
                print("Snowflake insertion failed:", error)
                print("Kafka offset was NOT committed.")
                print("Restart the consumer to retry this message.")
                break

    except KeyboardInterrupt:
        print("\nConsumer stopped.")

    finally:
        consumer.close()
        print("Kafka consumer connection closed.")
