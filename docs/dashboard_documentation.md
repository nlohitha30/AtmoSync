# AtmoSync – Micro-Climate Arbitrage Analytics

## 1. Project Overview

AtmoSync is an IoT-based micro-climate monitoring and commodity arbitrage analytics platform. It monitors environmental conditions inside commodity storage and transportation containers and analyzes commodity price differences across markets.

The system aims to help identify potential spoilage risks and profitable commodity trading opportunities using sensor data and analytics.

## 2. Project Objectives

- Monitor temperature, humidity, and vibration from IoT sensors.
- Validate and clean incoming sensor records.
- Store raw and transformed data in Snowflake.
- Process and transform data using dbt.
- Analyze commodity prices across different markets.
- Calculate potential arbitrage opportunities.
- Estimate net profit after transportation, storage, and spoilage costs.
- Display analytics through an interactive dashboard.

## 3. Technology Stack

| Technology | Purpose |
|---|---|
| Python | Backend logic and data processing |
| Streamlit | Interactive dashboard |
| Apache Kafka | Sensor event streaming |
| Snowflake | Cloud data warehouse |
| dbt | Data transformation |
| Pandas | Data analysis |
| Matplotlib | Data visualization |
| Git and GitHub | Version control |
| Docker | Containerized Kafka testing |

## 4. System Architecture

### Data Flow

1. IoT Sensor Simulator generates sample container sensor records.
2. Sensor Data Validator checks incoming records.
3. Apache Kafka handles sensor message streaming.
4. Snowflake stores raw sensor and commodity price data.
5. dbt transforms raw data into analytics-ready tables.
6. Python analytics modules calculate risk and arbitrage metrics.
7. Streamlit displays the results through an interactive dashboard.

**Note:** Kafka producer-consumer testing is complete. End-to-end automatic Kafka-to-Snowflake ingestion is still pending.

## 5. Dashboard Features

### 5.1 Sensor Monitoring
- Total sensor records.
- Average temperature.
- Average humidity.
- Temperature monitoring chart.
- Humidity monitoring chart.
- Vibration monitoring chart.
- Container sensor details table.

### 5.2 Spoilage Risk Monitoring

The prototype evaluates temperature, humidity, and vibration using a rule-based risk scoring approach.

Risk categories:
- LOW
- MEDIUM
- HIGH

**Note:** Current thresholds are demonstration assumptions and are not scientifically validated spoilage predictions.

### 5.3 Commodity Price Analytics

- Highest commodity price.
- Lowest commodity price.
- Market-wise commodity price comparison.
- Commodity-wise price analysis.

Current commodity price records are illustrative sample data, not live market feeds.

### 5.4 Arbitrage Opportunity Detection

The system compares commodity prices between Bengaluru and Tirupati to identify potential buy-low and sell-high opportunities.

It calculates:
- Buying market.
- Selling market.
- Gross price spread.
- Arbitrage percentage.

### 5.5 Net Profit and Rerouting Analysis

The calculator considers:
- Buying price.
- Selling price.
- Transportation cost.
- Storage cost.
- Estimated spoilage percentage.

It calculates estimated net profit per kilogram and provides a profitability indication.

## 6. Database Details

**Database:** ATMOSYNC_DB

**Raw Schema:** RAW_DATA

- SENSOR_DATA
- COMMODITY_PRICES

**Transformed Schema:** DBT_TRANSFORMED

- STG_SENSOR_DATA
- STG_COMMODITY_PRICES

## 7. Testing and Validation

Completed testing includes:

- Sensor data validation.
- Invalid humidity detection.
- Missing field detection.
- Negative vibration detection.
- Spoilage risk calculation tests.
- Kafka producer-consumer message verification.
- dbt model execution.
- dbt data quality tests.
- Snowflake connection verification.
- Streamlit dashboard execution.

Current Python test suite: **9 tests passed**.

Current dbt test suite: **13 tests passed**.

## 8. Current Implementation Status

- IoT sensor simulation: Completed.
- Sensor validation: Completed.
- Kafka producer-consumer testing: Completed.
- Snowflake raw data storage: Completed.
- dbt transformation models: Completed.
- Commodity price analytics: Completed.
- Arbitrage calculator: Completed.
- Net profit calculator: Completed.
- Prototype spoilage risk module: Completed.
- Streamlit dashboard: Implemented.
- Kafka-to-Snowflake automated integration: Pending.

## 9. Future Enhancements

- Implement automated Kafka-to-Snowflake ingestion.
- Integrate real IoT sensor devices.
- Connect live commodity market price feeds.
- Improve spoilage risk assessment using historical data and validated models.
- Implement automated rerouting recommendations.
- Add real-time notifications and alerts.
- Improve dashboard deployment and monitoring.

## 10. Conclusion

AtmoSync combines IoT sensor monitoring, cloud data warehousing, data transformation, and commodity price analytics into one dashboard.

The current implementation provides a working prototype for environmental monitoring, risk assessment, and commodity arbitrage analysis. Further development will focus on automated real-time data integration and intelligent rerouting recommendations.
