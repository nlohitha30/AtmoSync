
import streamlit as st
import pandas as pd
import os
import sys

# Add project root to Python path
PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)
sys.path.append(PROJECT_ROOT)
from src.spoilage_risk import calculate_spoilage_risk
from src.snowflake_connection import create_snowflake_connection
from src.arbitrage_calculator import calculate_arbitrage
from src.net_profit_calculator import calculate_net_profit

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

    # Spoilage Risk Monitoring
    st.divider()
    st.header("Spoilage Risk Monitoring")

    risk_results = sensor_data.apply(
        lambda row: calculate_spoilage_risk(
            temperature=float(row["TEMPERATURE_C"]),
            humidity=float(row["HUMIDITY_PCT"]),
            vibration=float(row["VIBRATION"])
        ),
        axis=1
    )

    sensor_data["RISK_SCORE"] = risk_results.apply(
        lambda result: result["risk_score"]
    )

    sensor_data["RISK_LEVEL"] = risk_results.apply(
        lambda result: result["risk_level"]
    )

    sensor_data["RISK_FACTORS"] = risk_results.apply(
        lambda result: ", ".join(result["risk_factors"])
        if result["risk_factors"] else "No elevated risk factors"
    )

    # Risk summary
    risk_counts = (
        sensor_data["RISK_LEVEL"]
        .value_counts()
        .reindex(["LOW", "MEDIUM", "HIGH"], fill_value=0)
    )

    col1, col2, col3 = st.columns(3)

    col1.metric("Low Risk Records", int(risk_counts["LOW"]))
    col2.metric("Medium Risk Records", int(risk_counts["MEDIUM"]))
    col3.metric("High Risk Records", int(risk_counts["HIGH"]))

    st.subheader("Container-wise Spoilage Risk")
    st.bar_chart(
        sensor_data.groupby("CONTAINER_ID")["RISK_SCORE"].mean()
    )

    st.subheader("Sensor Spoilage Risk Details")

    st.dataframe(
        sensor_data[
            [
                "CONTAINER_ID",
                "COMMODITY",
                "TEMPERATURE_C",
                "HUMIDITY_PCT",
                "VIBRATION",
                "RISK_SCORE",
                "RISK_LEVEL",
                "RISK_FACTORS"
            ]
        ],
        use_container_width=True
    )

    st.caption(
        "Note: Risk scores use prototype thresholds "
        "and are not scientifically validated predictions."
    )

    
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
        
    # Net Profit Analysis
    st.divider()
    st.header("Net Profit & Rerouting Analysis")

    profit_opportunities = calculate_arbitrage(commodity_data)

    if not profit_opportunities.empty:
        st.subheader("Select Commodity")

        selected_commodity = st.selectbox(
            "Choose commodity",
            profit_opportunities["COMMODITY"].tolist()
        )

        selected_row = profit_opportunities[
            profit_opportunities["COMMODITY"] == selected_commodity
        ].iloc[0]

        st.write(
            f"Buy from: **{selected_row['BUY_MARKET']}** "
            f"at ₹{selected_row['BUY_PRICE']:.2f}/kg"
        )

        st.write(
            f"Sell at: **{selected_row['SELL_MARKET']}** "
            f"at ₹{selected_row['SELL_PRICE']:.2f}/kg"
        )

        col1, col2, col3 = st.columns(3)

        with col1:
            transport_cost = st.number_input(
                "Transport cost (₹/kg)",
                min_value=0.0,
                value=0.40,
                step=0.10
            )

        with col2:
            storage_cost = st.number_input(
                "Storage cost (₹/kg)",
                min_value=0.0,
                value=0.20,
                step=0.10
            )

        with col3:
            spoilage_percentage = st.number_input(
                "Estimated spoilage (%)",
                min_value=0.0,
                max_value=100.0,
                value=1.0,
                step=0.5
            )

        result = calculate_net_profit(
            buy_price=float(selected_row["BUY_PRICE"]),
            sell_price=float(selected_row["SELL_PRICE"]),
            transport_cost=transport_cost,
            storage_cost=storage_cost,
            spoilage_percentage=spoilage_percentage
        )

        st.metric(
            "Net Profit per KG",
            f"₹{result['net_profit_per_kg']:.2f}"
        )

        if result["recommendation"] == "PROFITABLE":
            st.success("Potentially Profitable Opportunity")
        else:
            st.warning("Not Profitable with Current Cost Assumptions")

    else:
        st.warning("No arbitrage opportunities available.")


    st.caption("AtmoSync | Snowflake Connected Dashboard")

except Exception as error:
    st.error("Unable to load sensor data from Snowflake.")
    st.code(str(error))
    st.info(
    "Please verify Snowflake connectivity and "
    "the required dbt models."
)