
def calculate_net_profit(
    buy_price,
    sell_price,
    transport_cost,
    storage_cost,
    spoilage_percentage
):
    # Validate inputs
    if min(buy_price, sell_price, transport_cost, storage_cost) < 0:
        raise ValueError("Prices and costs cannot be negative")

    if not 0 <= spoilage_percentage <= 100:
        raise ValueError("Spoilage percentage must be between 0 and 100")

    # Calculate revenue after spoilage
    effective_sell_price = sell_price * (
        1 - spoilage_percentage / 100
    )

    # Calculate total cost
    total_cost = buy_price + transport_cost + storage_cost

    # Calculate net profit per purchased kg
    net_profit = effective_sell_price - total_cost

    return {
        "buy_price": buy_price,
        "effective_sell_price": effective_sell_price,
        "transport_cost": transport_cost,
        "storage_cost": storage_cost,
        "spoilage_percentage": spoilage_percentage,
        "net_profit_per_kg": round(net_profit, 2),
        "recommendation": (
            "PROFITABLE" if net_profit > 0
            else "NOT PROFITABLE"
        )
    }


if __name__ == "__main__":
    result = calculate_net_profit(
        buy_price=42.5,
        sell_price=44.0,
        transport_cost=0.40,
        storage_cost=0.20,
        spoilage_percentage=1
    )

    print("\nAtmoSync Net Profit Analysis")

    for key, value in result.items():
        print(f"{key}: {value}")
