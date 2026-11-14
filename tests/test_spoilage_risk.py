
from src.spoilage_risk import calculate_spoilage_risk


def test_low_spoilage_risk():
    result = calculate_spoilage_risk(20, 40, 1)

    assert result["risk_score"] == 0
    assert result["risk_level"] == "LOW"


def test_medium_spoilage_risk():
    result = calculate_spoilage_risk(35, 40, 1)

    assert result["risk_score"] == 40
    assert result["risk_level"] == "MEDIUM"


def test_high_spoilage_risk():
    result = calculate_spoilage_risk(35, 80, 4)

    assert result["risk_score"] == 100
    assert result["risk_level"] == "HIGH"


def test_temperature_risk_factor():
    result = calculate_spoilage_risk(35, 40, 1)

    assert "High temperature" in result["risk_factors"]


def test_humidity_risk_factor():
    result = calculate_spoilage_risk(20, 80, 1)

    assert "High humidity" in result["risk_factors"]


def test_vibration_risk_factor():
    result = calculate_spoilage_risk(20, 40, 4)

    assert "High vibration" in result["risk_factors"]
