
import os
import json
from kafka import KafkaConsumer

KAFKA_SERVER = os.getenv("KAFKA_SERVER", "localhost:9094")
KAFKA_TOPIC = "atmosync-sensor-data"


def deserialize_sensor_message(message):
    """Safely deserialize a Kafka sensor message."""
    try:
        return json.loads(message.decode("utf-8"))

    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        print(f"Rejected invalid Kafka message: {error}")
        return None


def create_consumer():
    consumer = KafkaConsumer(
        KAFKA_TOPIC,
        bootstrap_servers=[KAFKA_SERVER],
        auto_offset_reset="earliest",
        enable_auto_commit=True,
        group_id="atmosync-consumer-group",
        value_deserializer=deserialize_sensor_message
    )
    return consumer


if __name__ == "__main__":
    print("AtmoSync Kafka Consumer Started")

    consumer = create_consumer()

    try:
        for message in consumer:
            if message.value is None:
                continue

            print("\nSensor Data Received:")
            print(json.dumps(message.value, indent=4))

    except KeyboardInterrupt:
        print("\nConsumer stopped.")

    finally:
        consumer.close()
