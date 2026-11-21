
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


# Additional boundary and score tests


def test_values_at_exact_thresholds_have_no_risk():
    result = calculate_spoilage_risk(30, 70, 3)

    assert result["risk_score"] == 0
    assert result["risk_level"] == "LOW"
    assert result["risk_factors"] == []


def test_humidity_risk_score():
    result = calculate_spoilage_risk(20, 80, 1)

    assert result["risk_score"] == 35
    assert result["risk_level"] == "MEDIUM"


def test_vibration_risk_score():
    result = calculate_spoilage_risk(20, 40, 4)

    assert result["risk_score"] == 25
    assert result["risk_level"] == "LOW"


def test_temperature_and_humidity_combined_risk():
    result = calculate_spoilage_risk(35, 80, 1)

    assert result["risk_score"] == 75
    assert result["risk_level"] == "HIGH"
    assert "High temperature" in result["risk_factors"]
    assert "High humidity" in result["risk_factors"]
