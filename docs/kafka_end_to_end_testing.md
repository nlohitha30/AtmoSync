
Kafka End-to-End Integration Testing

1. Overview

This document describes the Kafka end-to-end integration testing performed for the AtmoSync project.

The testing verifies:

Kafka broker connectivity.

Sensor data production using the Python Kafka producer.

Message delivery to the Kafka topic.

Message verification using the Kafka consumer.

Sensor data validation for valid and invalid inputs.

2. Kafka Environment Setup

Kafka Version: Apache Kafka 4.4.0

Docker Image: apache/kafka:4.4.0

Container Name: atmosync-kafka

Kafka Broker: localhost:9092

Kafka Topic: atmosync-sensor-data

Start Kafka Broker

Pull the Kafka Docker image:

docker pull apache/kafka:4.4.0

Start the Kafka container:

docker run -d --name atmosync-kafka -p 9092:9092 apache/kafka:4.4.0

Verify the running container:

docker ps

Verify Kafka Topic

docker exec -it atmosync-kafka /opt/kafka/bin/kafka-topics.sh --bootstrap-server localhost:9092 --list

Expected topic:

__consumer_offsets
atmosync-sensor-data

3. Kafka Producer Testing

Producer file: src/kafka_producer.py

Run the producer:

python src/kafka_producer.py

The producer generates sensor readings containing:

container_id

commodity

temperature_c

humidity_pct

vibration

timestamp

The producer sends these readings as JSON messages to the Kafka topic atmosync-sensor-data.

Result: Producer successfully sent sensor messages to Kafka.

4. Kafka Consumer Testing

Run the Kafka console consumer:

docker exec -it atmosync-kafka /opt/kafka/bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic atmosync-sensor-data --from-beginning

Successful Message Verification

The consumer successfully received JSON sensor messages.

Sample verified reading:

{
  "container_id": "CONT004",
  "commodity": "Coffee",
  "temperature_c": 26.44,
  "humidity_pct": 55.09,
  "vibration": 3.17,
  "timestamp": "2026-11-13T15:37:16.330798+00:00"
}

Other received readings included:

CONT002 – Wheat

CONT003 – Corn

CONT001 – Rice

CONT004 – Coffee

Result: Successfully verified that sensor messages were delivered to the Kafka topic and retrieved by the consumer.

5. Sensor Data Validation Testing

Validator file: src/sensor_data_validator.py

Test file: tests/test_sensor_data_validator.py

The sensor data validator checks whether incoming sensor readings contain valid fields and values.

Test Cases

Test Case

Expected Result

Valid sensor data

PASS

Missing required field

PASS

Humidity value -10

PASS

Humidity value 101

PASS

Negative vibration

PASS

PASS means the test successfully verified the expected validation behavior. Invalid input values are correctly rejected by the validator.

Execute Tests

pytest -v tests/test_sensor_data_validator.py

Test Execution Result

tests/test_sensor_data_validator.py::test_valid_sensor_data PASSED
tests/test_sensor_data_validator.py::test_missing_required_field PASSED
tests/test_sensor_data_validator.py::test_invalid_humidity[-10] PASSED
tests/test_sensor_data_validator.py::test_invalid_humidity[101] PASSED
tests/test_sensor_data_validator.py::test_negative_vibration PASSED

===================== 5 passed in 0.07s =====================

Result: All five sensor data validation tests passed successfully.

6. Docker Network Configuration and Limitations

Kafka was deployed using Docker with the following configuration:

Container name: atmosync-kafka

Published port: 9092:9092

Kafka image: apache/kafka:4.4.0

Bootstrap address used by the host-based Python producer: localhost:9092

The container was started without an explicit --network option. Therefore, Docker's default bridge network was used.

Network Limitations

The Kafka port must be published to allow the host application to connect.

localhost refers to the host when used by the host-based producer.

Inside another container, localhost refers to that container itself, not the Kafka broker.

The current setup does not configure a dedicated user-defined Docker network or Docker Compose environment.

Container-to-container communication and advertised-listener configuration have not been independently verified.

A dedicated Docker network and appropriate Kafka listener configuration would be required for a fully containerized producer-consumer deployment.

7. Kafka-to-Snowflake Integration Status

Status: Pending

Kafka producer and consumer testing has been completed successfully.

However, the complete Kafka-to-Snowflake integration is still pending.

The following work remains:

Connect the Kafka consumer or streaming process to Snowflake.

Configure the Snowflake connection.

Transfer Kafka sensor messages into Snowflake tables.

Verify successful data insertion and retrieval.

The Kafka-to-Snowflake integration has not yet been completed or verified.

8. Final Conclusion

Kafka end-to-end testing was successfully performed for the AtmoSync project.

The following activities were completed:

Kafka broker started using Docker.

Kafka topic verified successfully.

Python Kafka producer executed.

Sensor messages received and verified using the Kafka consumer.

Valid and invalid sensor data validation tested.

All five validation tests passed.

Testing process and results documented.



Overall Result: Kafka producer, consumer, and sensor data validation testing completed successfully.