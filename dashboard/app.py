
import streamlit as st
import pandas as pd
import os
import sys

# Add project root to Python path
PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)
sys.path.append(PROJECT_ROOT)

from src.snowflake_connection import create_snowflake_connection

# Page configuration
st.set_page_config(
    page_title="AtmoSync Dashboard",
    page_icon="🌦️",
    layout="wide"
)

st.title("AtmoSync - Micro-Climate Arbitrage Analytics")
st.markdown("### Live IoT Sensor Monitoring Dashboard")
st.divider()

# Sidebar
st.sidebar.title("AtmoSync Navigation")
st.sidebar.write("Dashboard Overview")
st.sidebar.write("Sensor Monitoring")
st.sidebar.write("Commodity Analytics")

# Load sensor data from Snowflake
@st.cache_data(ttl=60)
def load_sensor_data():
    connection = create_snowflake_connection()
    cursor = connection.cursor()

    try:
        query = """
            SELECT
                CONTAINER_ID,
                COMMODITY,
                TEMPERATURE_C,
                HUMIDITY_PCT,
                VIBRATION,
                TIMESTAMP AS SENSOR_TIMESTAMP
            FROM ATMOSYNC_DB.DBT_TRANSFORMED.STG_SENSOR_DATA
            ORDER BY TIMESTAMP DESC
        """

        cursor.execute(query)
        rows = cursor.fetchall()

        columns = [column[0] for column in cursor.description]

        return pd.DataFrame(rows, columns=columns)

    finally:
        cursor.close()
        connection.close()

@st.cache_data(ttl=60)
def load_commodity_data():
    connection = create_snowflake_connection()
    cursor = connection.cursor()

    try:
        query = """
            SELECT
                COMMODITY,
                MARKET,
                PRICE_PER_KG,
                CURRENCY,
                UNIT,
                PRICE_DATE,
                DATA_SOURCE
            FROM ATMOSYNC_DB.DBT_TRANSFORMED.STG_COMMODITY_PRICES
            ORDER BY MARKET, COMMODITY
        """

        cursor.execute(query)
        rows = cursor.fetchall()

        columns = [column[0] for column in cursor.description]

        return pd.DataFrame(rows, columns=columns)

    finally:
        cursor.close()
        connection.close()


# Display dashboard
try:
    sensor_data = load_sensor_data()

    if sensor_data.empty:
        st.warning("No sensor records found in Snowflake.")
        st.stop()

    # KPI Cards
    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Total Sensor Records",
        len(sensor_data)
    )

    col2.metric(
        "Average Temperature",
        f"{sensor_data['TEMPERATURE_C'].mean():.2f} °C"
    )

    col3.metric(
        "Average Humidity",
        f"{sensor_data['HUMIDITY_PCT'].mean():.2f} %"
    )

    st.divider()

    
    # Container-wise sensor analytics
    container_data = sensor_data.groupby("CONTAINER_ID").agg({
        "TEMPERATURE_C": "mean",
        "HUMIDITY_PCT": "mean",
        "VIBRATION": "mean"
    }).round(2)

    # Temperature chart
    st.subheader("Temperature Monitoring")
    st.bar_chart(container_data["TEMPERATURE_C"])

    # Humidity chart
    st.subheader("Humidity Monitoring")
    st.bar_chart(container_data["HUMIDITY_PCT"])

    # Vibration chart
    st.subheader("Vibration Monitoring")
    st.bar_chart(container_data["VIBRATION"])

    # Container details
    st.subheader("Container Sensor Details")

    display_data = sensor_data.rename(columns={
        "CONTAINER_ID": "Container",
        "COMMODITY": "Commodity",
        "TEMPERATURE_C": "Temperature (°C)",
        "HUMIDITY_PCT": "Humidity (%)",
        "VIBRATION": "Vibration",
        "SENSOR_TIMESTAMP": "Timestamp"
    })

    # Commodity Price Analytics
    st.divider()
    st.header("Commodity Price Analytics")

    commodity_data = load_commodity_data()

    if not commodity_data.empty:

        # Highest and lowest price
        highest_price = commodity_data.loc[
            commodity_data["PRICE_PER_KG"].idxmax()
        ]

        lowest_price = commodity_data.loc[
            commodity_data["PRICE_PER_KG"].idxmin()
        ]

        col1, col2 = st.columns(2)

        col1.metric(
            "Highest Commodity Price",
            f"₹{highest_price['PRICE_PER_KG']:.2f}/kg",
            f"{highest_price['COMMODITY']} - {highest_price['MARKET']}"
        )

        col2.metric(
            "Lowest Commodity Price",
            f"₹{lowest_price['PRICE_PER_KG']:.2f}/kg",
            f"{lowest_price['COMMODITY']} - {lowest_price['MARKET']}"
        )

        # Market-wise price comparison
        st.subheader("Market-wise Commodity Price Comparison")

        price_comparison = commodity_data.pivot_table(
    index="COMMODITY",
    columns="MARKET",
    values="PRICE_PER_KG",
    aggfunc="mean"
)

        st.bar_chart(price_comparison)

        
        # Arbitrage Opportunity Analysis
        st.subheader("Arbitrage Opportunity Detection")

        arbitrage_data = commodity_data.pivot_table(
            index="COMMODITY",
            columns="MARKET",
            values="PRICE_PER_KG",
            aggfunc="mean"
        )

        # Identify available market prices
        market_columns = list(arbitrage_data.columns)

        if len(market_columns) >= 2:

            arbitrage_data["Lowest Market"] = (
                arbitrage_data[market_columns].idxmin(axis=1)
            )

            arbitrage_data["Highest Market"] = (
                arbitrage_data[market_columns].idxmax(axis=1)
            )

            arbitrage_data["Price Difference"] = (
                arbitrage_data[market_columns].max(axis=1)
                - arbitrage_data[market_columns].min(axis=1)
            ).round(2)

            arbitrage_data["Price Difference (%)"] = (
                arbitrage_data["Price Difference"]
                / arbitrage_data[market_columns].min(axis=1)
                * 100
            ).round(2)

            st.dataframe(
                arbitrage_data,
                use_container_width=True
            )

            st.bar_chart(
                arbitrage_data["Price Difference"]
            )

        else:
            st.warning("At least two markets are required.")

    st.caption("AtmoSync | Snowflake Connected Dashboard")

except Exception as error:
    st.error("Unable to load sensor data from Snowflake.")
    st.code(str(error))
    st.info(
    "Please verify Snowflake connectivity and "
    "the required dbt models."
)