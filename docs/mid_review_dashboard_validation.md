\# AtmoSync Mid-Review Dashboard Validation



\## Date

16 November 2026



\## Dashboard Status

The AtmoSync Streamlit dashboard was successfully launched and connected to Snowflake.



\## Verified KPI Metrics

\- Total Sensor Records: 7

\- Average Temperature: 29.44 °C

\- Average Humidity: 56.80%



\## Verified Dashboard Features

\- Temperature monitoring chart

\- Humidity monitoring chart

\- Vibration monitoring chart

\- Spoilage risk monitoring

\- Commodity price comparison

\- Arbitrage opportunity detection

\- Net profit and rerouting analysis

\- Container-wise sensor details table



\## Container Sensor Details

The dashboard displays seven sensor records with:

\- Container ID

\- Commodity

\- Temperature

\- Humidity

\- Vibration

\- Timestamp

\- Risk Score

\- Risk Level

\- Risk Factors



\## Commodity Analytics

\- Highest price: Coffee – Bengaluru, ₹340/kg

\- Lowest price: Corn – Tirupati, ₹28/kg

\- Net profit example: ₹16/kg



\## Remaining Work

\- Complete Python and dbt testing.

\- Verify all dashboard calculations.

\- Complete final integration checks.

\- Prepare the mid-review demonstration.



\## Conclusion

The main AtmoSync dashboard features are implemented and displaying data. Final testing and review preparation are in progress.


## November 18, 2026 - Mid-Review Test Results

### Python Validation
- Dashboard syntax check completed successfully.
- Python test suite: 9 tests passed.
- Sensor data validation tests passed.
- Spoilage risk calculation tests passed.

### dbt Validation
- Total dbt data tests: 13.
- Passed: 13.
- Failed: 0.
- Warnings: 0.
- dbt execution completed successfully.

### Dashboard Performance Optimization
- Sensor data caching configured with a 300-second TTL.
- Commodity data caching configured with a 300-second TTL.
- Spoilage risk calculations moved into a cached function.
- Duplicate spoilage risk calculations removed.

### Conclusion
Python and dbt validation completed successfully on November 18, 2026. Dashboard data loading and spoilage risk calculations have been optimized. The project is prepared for mid-review validation.

