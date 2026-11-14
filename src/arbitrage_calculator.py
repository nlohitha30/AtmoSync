
import pandas as pd


def calculate_arbitrage(price_data):
    """
    Calculate commodity-wise arbitrage opportunities.
    """

    if price_data.empty:
        return pd.DataFrame()

    required_columns = ["COMMODITY", "MARKET", "PRICE_PER_KG"]

    for column in required_columns:
        if column not in price_data.columns:
            raise ValueError(f"Missing required column: {column}")

    # Group prices by commodity and market
    grouped = price_data.pivot_table(
        index="COMMODITY",
        columns="MARKET",
        values="PRICE_PER_KG",
        aggfunc="mean"
    )

    results = []

    for commodity, prices in grouped.iterrows():
        valid_prices = prices.dropna()

        if len(valid_prices) < 2:
            continue

        lowest_market = valid_prices.idxmin()
        highest_market = valid_prices.idxmax()

        lowest_price = valid_prices.min()
        highest_price = valid_prices.max()

        spread = highest_price - lowest_price

        arbitrage_percentage = (
            spread / lowest_price
        ) * 100

        results.append({
            "COMMODITY": commodity,
            "BUY_MARKET": lowest_market,
            "SELL_MARKET": highest_market,
            "BUY_PRICE": lowest_price,
            "SELL_PRICE": highest_price,
            "GROSS_SPREAD": spread,
            "ARBITRAGE_PERCENTAGE": arbitrage_percentage
        })

    return pd.DataFrame(results)


if __name__ == "__main__":
    sample_data = pd.DataFrame({
        "COMMODITY": ["Rice", "Rice", "Wheat", "Wheat"],
        "MARKET": ["Tirupati", "Bengaluru", "Tirupati", "Bengaluru"],
        "PRICE_PER_KG": [42.5, 44, 35, 37]
    })

    result = calculate_arbitrage(sample_data)

    print("\nAtmoSync Arbitrage Analysis")
    print(result.to_string(index=False))
