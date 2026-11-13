# AtmoSync – Kafka Integration Testing

## 1. Objective

To implement and verify real-time IoT sensor data streaming using Apache Kafka in the AtmoSync project.

## 2. Architecture

IoT Sensor Simulator → Kafka Producer → Kafka Broker → Kafka Consumer

## 3. Technologies Used

- Python 3.11
- Apache Kafka 3.9.0
- kafka-python 3.0.13
- Docker
- JSON

## 4. Kafka Configuration

- Kafka Topic: `atmosync-sensor-data`
- Broker container: `order-kafka`
- Kafka network: `real-time-order-processing-system_default`
- Bootstrap server inside Docker network: `kafka:9092`
- Partitions: 1
- Replication factor: 1

## 5. Producer Implementation

File: `src/kafka_producer.py`

The Kafka producer:
- Generates IoT sensor data using the sensor simulator.
- Converts sensor data into JSON messages.
- Publishes messages to the `atmosync-sensor-data` topic.
- Uses acknowledgements and retries for message delivery.

## 6. Consumer Implementation

File: `src/kafka_consumer.py`

The Kafka consumer:
- Subscribes to the `atmosync-sensor-data` topic.
- Receives JSON sensor messages.
- Deserializes messages into Python dictionaries.
- Displays received sensor information.

## 7. Testing Procedure

### Test 1: Kafka Producer

Executed the producer inside the Kafka Docker network.

Verified that messages were successfully published to the Kafka topic.

### Test 2: Kafka Broker

Created the `atmosync-sensor-data` topic with one partition and one replica.

### Test 3: Kafka Console Consumer

Used the Kafka console consumer to read messages from the topic.

Result: Successfully processed 5 messages.

### Test 4: Python Kafka Consumer

Executed `src/kafka_consumer.py` inside the Kafka Docker network.

Result: Successfully received and displayed sensor messages.

## 8. Sample Received Sensor Data

```json
{
  "container_id": "CONT003",
  "commodity": "Corn",
  "temperature_c": 20.71,
  "humidity_pct": 53.05,
  "vibration": 2.65,
  "timestamp": "2026-11-13T15:23:35.738816+00:00"
}
```

## 9. Testing Results

| Component | Result |
|---|---|
| Kafka Topic Creation | Successful |
| Producer Message Publishing | Successful |
| Kafka Broker Communication | Successful |
| Console Consumer | Successful |
| Python Consumer | Successful |
| End-to-End Message Flow | Verified |

## 10. Important Configuration Note

The existing Kafka broker advertises `kafka:9092`, which is accessible from containers