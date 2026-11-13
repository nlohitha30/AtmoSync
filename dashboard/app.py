
import streamlit as st
import pandas as pd

# Page configuration
st.set_page_config(
    page_title="AtmoSync Dashboard",
    page_icon="🌦️",
    layout="wide"
)

# Dashboard title
st.title("🌦️ AtmoSync - Micro-Climate Arbitrage Analytics")
st.markdown("### Real-Time IoT Sensor Monitoring Dashboard")

st.divider()

# Sidebar
st.sidebar.title("AtmoSync Navigation")
st.sidebar.write("Dashboard Overview")
st.sidebar.write("Sensor Monitoring")
st.sidebar.write("Commodity Analytics")

# KPI Cards - Sample data for initial UI
col1, col2, col3 = st.columns(3)

col1.metric("Total Sensor Records", "7")
col2.metric("Average Temperature", "29.44 °C")
col3.metric("Average Humidity", "62.5 %")

st.divider()

# Sample sensor data
sensor_data = pd.DataFrame({
    "Container": ["CONT001", "CONT002", "CONT003", "CONT004"],
    "Commodity": ["Rice", "Wheat", "Corn", "Coffee"],
    "Temperature": [28.37, 28.07, 29.32, 33.63],
    "Humidity": [65.2, 60.5, 53.05, 70.1],
    "Vibration": [1.2, 2.1, 2.65, 3.4]
})

# Charts
st.subheader("🌡️ Temperature Monitoring")
st.line_chart(sensor_data.set_index("Container")["Temperature"])

st.subheader("💧 Humidity Monitoring")
st.bar_chart(sensor_data.set_index("Container")["Humidity"])

st.subheader("📦 Container Sensor Details")
st.dataframe(sensor_data, use_container_width=True)

st.caption("AtmoSync | Initial Dashboard Prototype")
