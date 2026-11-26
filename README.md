# 🌦️ AtmoSync – Micro-Climate Arbitrage Analytics Platform

## 1. Project Overview

AtmoSync is a Python-based data analytics platform that combines weather information and IoT sensor data to monitor micro-climate conditions, analyze commodity prices, identify potential arbitrage opportunities, and assess commodity spoilage risk.

The platform integrates weather data collection, sensor data processing, Kafka messaging, Snowflake data storage, dbt transformations, and an interactive Streamlit dashboard.

## 2. Project Objectives

- Collect weather data from multiple geographical locations.
- Monitor IoT sensor readings from commodity storage containers.
- Process and validate sensor data.
- Store structured data in Snowflake.
- Transform data using dbt.
- Analyze temperature, humidity, rainfall, wind, and vibration.
- Compare commodity prices across locations.
- Identify potential arbitrage opportunities.
- Estimate spoilage risk using sensor readings.
- Calculate potential net profit from commodity rerouting.
- Present analytics through an interactive dashboard.

## 3. Technologies Used

| Category | Technologies |
|---|---|
| Programming | Python |
| Data Processing | Pandas, NumPy |
| Weather API | Open-Meteo API |
| Dashboard | Streamlit |
| Visualization | Plotly |
| Messaging | Apache Kafka |
| Containerization | Docker |
| Data Warehouse | Snowflake |
| Data Transformation | dbt |
| Testing | Pytest |
| Version Control | Git and GitHub |

## 4. Data Sources

### Weather Data

Weather information is collected using the Open-Meteo API.

Locations monitored:
- Tirupati
- Bengaluru
- Chennai
- Hyderabad

Weather parameters include:
- Temperature
- Humidity
- Rainfall
- Wind speed

API: https://open-meteo.com/

### IoT Sensor Data

The project uses simulated IoT sensor readings for commodity storage containers.

Sensor fields include:
- `container_id`
- `commodity`
- `temperature_c`
- `humidity_pct`
- `vibration`
- `timestamp`

Sample commodities include Rice, Wheat, Corn, and Coffee.

## 5. Data Pipeline Architecture

The AtmoSync data pipeline follows these major stages:

1. **Data Collection:** Collect weather information and generate IoT sensor readings.
2. **Data Validation:** Validate incoming sensor records and check required fields and acceptable values.
3. **Kafka Integration:** Produce and consume sensor messages using Apache Kafka.
4. **Data Storage:** Store sensor and commodity information in Snowflake.
5. **Data Transformation:** Use dbt to transform raw data into analytics-ready datasets.
6. **Data Analysis:** Analyze sensor conditions, commodity prices, spoilage risk, and arbitrage opportunities.
7. **Visualization:** Display results through the Streamlit dashboard.

## 6. Dashboard Features

The AtmoSync dashboard is developed using Streamlit.

### Dashboard Overview
- Total sensor records
- Average temperature
- Average humidity
- Key project metrics

### Sensor Monitoring
- Container-wise sensor information
- Temperature monitoring
- Humidity monitoring
- Vibration monitoring
- Spoilage risk classification
- Container-wise risk visualization

### Commodity Analytics
- Commodity price comparison
- Highest and lowest commodity prices
- Location-wise market comparison
- Arbitrage opportunity identification
- Net profit calculation
- Commodity rerouting analysis

### Spoilage Risk Monitoring

The project uses temperature, humidity, and vibration readings to calculate a prototype spoilage risk score.

Risk categories:
- Low
- Medium
- High

**Note:** The spoilage risk thresholds are prototype rules and are not scientifically validated predictions.

## 7. Kafka Integration

Apache Kafka is used for sensor data messaging.

Kafka topic:

`atmosync-sensor-data`

The Python producer sends sensor readings to the Kafka topic, and the consumer receives the messages for verification and processing.

Docker is used to run the Kafka environment.

## 8. Snowflake and dbt Integration

Snowflake is used as the project's cloud data warehouse.

Database: `ATMOSYNC_DB`

Schemas:
- `RAW_DATA`
- `DBT_TRANSFORMED`

dbt is used to transform raw sensor data and perform data quality tests.

## 9. Testing and Validation

Testing is performed to improve data reliability and application quality.

- Sensor data validation tests
- Invalid sensor input tests
- Kafka producer and consumer verification
- dbt data quality tests
- Spoilage risk calculation tests
- Python application compilation checks

Run Python tests using:

```powershell
python -m pytest -v
```

## 10. Project Structure

```text
AtmoSync/
│
├── dashboard/
│   ├── app.py
│   ├── header.html
│   └── style.css
│
├── data/
│
├── docs/
│   ├── dashboard_documentation.md
│   ├── kafka_integration_testing.md
│   ├── sensor_data_schema.md
│   └── week1_integration_status.md
│
├── src/
│   ├── kafka_producer.py
│   ├── spoilage_risk.py
│   └── snowflake_connection.py
│
├── tests/
│
├── requirements.txt
└── README.md
```

## 11. Running the Dashboard

### Step 1: Clone the repository

```powershell
git clone https://github.com/nlohitha30/AtmoSync.git
```

### Step 2: Open the project folder

```powershell
cd AtmoSync
```

### Step 3: Create a virtual environment

```powershell
py -3.11 -m venv .venv
```

### Step 4: Activate the virtual environment

```powershell
.\.venv\Scripts\Activate.ps1
```

### Step 5: Install dependencies

```powershell
python -m pip install -r requirements.txt
```

### Step 6: Run the Streamlit dashboard

```powershell
streamlit run dashboard/app.py
```

The dashboard will be available at:

http://localhost:8501

**Note:** Configure the required Snowflake connection settings before running features that access Snowflake. Do not commit passwords, account credentials, or other secrets to GitHub.

## 12. Current Project Status

The project has progressed beyond initial setup and includes:

- Weather data collection using Open-Meteo.
- IoT sensor data simulation and validation.
- Kafka producer and consumer integration using Apache Kafka.
- Sensor message validation before database insertion.
- Validated Kafka sensor records stored in Snowflake.
- Manual Kafka offset commits after successful processing.
- dbt transformations and data quality testing.
- Commodity price analytics and arbitrage calculations.
- Prototype spoilage risk monitoring.
- Interactive Streamlit analytics dashboard.

### Kafka-to-Snowflake Processing Flow

1. The Kafka producer publishes sensor messages to the `atmosync-sensor-data` topic.
2. The Kafka consumer receives incoming messages.
3. Sensor records are validated before processing.
4. Valid records are inserted into the `ATMOSYNC_DB.RAW_DATA.SENSOR_DATA` table.
5. Kafka offsets are committed after successful processing.
6. If Snowflake insertion fails, the offset is not committed.
7. Invalid sensor messages are rejected.

**Integration verification:** A sample sensor record was successfully processed and verified in Snowflake.

**Test command:**

```powershell
python -m pytest -v