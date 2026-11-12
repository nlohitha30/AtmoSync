
import json
import time
from kafka import KafkaProducer
from iot_sensor_simulator import generate_sensor_data

# Kafka broker address
KAFKA_SERVER = "localhost:9092"

# Kafka topic
KAFKA_TOPIC = "atmosync-sensor-data"


def create_producer():
    producer = KafkaProducer(
        bootstrap_servers=[KAFKA_SERVER],
        value_serializer=lambda data: json.dumps(data).encode("utf-8"),
        acks="all",
        retries=5
    )
    return producer


if __name__ == "__main__":

    print("AtmoSync Kafka Producer Started")

    producer = create_producer()

    try:
        while True:

            # Generate sensor data
            data = generate_sensor_data()

            # Send data to Kafka
            future = producer.send(KAFKA_TOPIC, value=data)

            # Confirm message delivery
            metadata = future.get(timeout=10)

            print("Message sent successfully!")
            print("Topic:", metadata.topic)
            print("Partition:", metadata.partition)
            print(json.dumps(data, indent=4))

            time.sleep(2)

    except KeyboardInterrupt:
        print("Producer stopped.")

    finally:
        producer.flush()
        producer.close()

