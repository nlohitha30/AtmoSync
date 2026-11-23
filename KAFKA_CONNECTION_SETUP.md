# Kafka External Connection Setup

AtmoSync connects to Kafka running in Docker.

## Kafka Listeners
- Port 9092: Internal Docker communication.
- Port 9094: External connection for AtmoSync on Windows.

## AtmoSync Configuration
Set the Kafka server before starting the producer:
`$env:KAFKA_SERVER = "localhost:9094"
python .\src\kafka_producer.py

## Connection Verification
Run Test-NetConnection localhost -Port 9094.
A successful connection displays TcpTestSucceeded : True.
