
import pandas as pd
import plotly.express as px
from pathlib import Path

# Project paths
BASE_DIR = Path(__file__).resolve().parent.parent
INPUT_FILE = BASE_DIR / "data" / "raw" / "commodity_prices.csv"
OUTPUT_FILE = BASE_DIR / "processed" / "commodity_price_summary.csv"
CHART_FILE = BASE_DIR / "static" / "charts" / "commodity_price_comparison.html"

REQUIRED_COLUMNS = [
    "COMMODITY", "MARKET", "PRICE_PER_KG",
    "CURRENCY", "UNIT", "PRICE_DATE", "DATA_SOURCE"
]


def analyze_commodity_prices():
    # Read dataset
    df = pd.read_csv(INPUT_FILE)

    # Validate required columns
    missing_columns = [
        col for col in REQUIRED_COLUMNS if col not in df.columns
    ]
    if missing_columns:
        raise ValueError(f"Missing columns: {missing_columns}")

    # Validate data
    df["PRICE_PER_KG"] = pd.to_numeric(
        df["PRICE_PER_KG"], errors="coerce"
    )
    df["PRICE_DATE"] = pd.to_datetime(
        df["PRICE_DATE"], errors="coerce"
    )

    df = df.dropna(subset=REQUIRED_COLUMNS)
    df = df[df["PRICE_PER_KG"] > 0]
    df = df[
        (df["CURRENCY"] == "INR") &
        (df["UNIT"] == "KG")
    ]

    if df.empty:
        raise ValueError("No valid commodity price records found.")

    # Remove duplicate records
    df = df.drop_duplicates(
        subset=["COMMODITY", "MARKET", "PRICE_DATE"]
    )

    # Commodity-wise price summary
    summary = df.groupby("COMMODITY").agg(
        average_price=("PRICE_PER_KG", "mean"),
        minimum_price=("PRICE_PER_KG", "min"),
        maximum_price=("PRICE_PER_KG", "max"),
        price_difference=("PRICE_PER_KG", lambda x: x.max() - x.min()),
        market_count=("MARKET", "nunique")
    ).reset_index()

    summary.to_csv(OUTPUT_FILE, index=False)

    # Create market-wise comparison chart
    fig = px.bar(
        df,
        x="COMMODITY",
        y="PRICE_PER_KG",
        color="MARKET",
        barmode="group",
        title="Commodity Price Comparison Across Markets",
        labels={
            "COMMODITY": "Commodity",
            "PRICE_PER_KG": "Price per KG (INR)",
            "MARKET": "Market"
        },
        text="PRICE_PER_KG"
    )

    fig.write_html(CHART_FILE)

    print("COMMODITY PRICE ANALYSIS")
    print("========================")
    print("Valid records:", len(df))
    print("\nCommodity-wise summary:")
    print(summary.to_string(index=False))
    print("\nSummary saved to:", OUTPUT_FILE)
    print("Chart saved to:", CHART_FILE)


if __name__ == "__main__":
    analyze_commodity_prices()
