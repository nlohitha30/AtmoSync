import pytest

from src.net_profit_calculator import calculate_net_profit


def test_profitable_opportunity():
    result = calculate_net_profit(
        buy_price=320,
        sell_price=340,
        transport_cost=0.40,
        storage_cost=0.20,
        spoilage_percentage=1
    )

    assert result["net_profit_per_kg"] == 16.00
    assert result["recommendation"] == "PROFITABLE"


def test_loss_making_opportunity():
    result = calculate_net_profit(
        buy_price=100,
        sell_price=90,
        transport_cost=5,
        storage_cost=2,
        spoilage_percentage=1
    )

    assert result["net_profit_per_kg"] < 0
    assert result["recommendation"] == "NOT PROFITABLE"


def test_zero_spoilage():
    result = calculate_net_profit(
        buy_price=100,
        sell_price=120,
        transport_cost=5,
        storage_cost=2,
        spoilage_percentage=0
    )

    assert result["effective_sell_price"] == 120
    assert result["net_profit_per_kg"] == 13


def test_negative_cost_is_rejected():
    with pytest.raises(ValueError):
        calculate_net_profit(
            buy_price=-100,
            sell_price=120,
            transport_cost=5,
            storage_cost=2,
            spoilage_percentage=1
        )


def test_invalid_spoilage_percentage_is_rejected():
    with pytest.raises(ValueError):
        calculate_net_profit(
            buy_price=100,
            sell_price=120,
            transport_cost=5,
            storage_cost=2,
            spoilage_percentage=101
        )