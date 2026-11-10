import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="AtmoSync Dashboard",
    page_icon="🌤️",
    layout="wide"
)

st.title("🌤️ AtmoSync")
st.subheader("Micro-Climate Arbitrage Analytics")

st.write("Welcome to the AtmoSync Weather Analytics Dashboard!")

st.info("Dashboard is running successfully!")

st.header("Weather Monitoring")

locations = ["Tirupati", "Bengaluru", "Chennai", "Hyderabad"]

city = st.selectbox("Select Location", locations)

st.write("Selected Location:", city)

st.success("AtmoSync application is working!")