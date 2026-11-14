
def calculate_spoilage_risk(
    temperature,
    humidity,
    vibration,
    temperature_limit=30,
    humidity_limit=70,
    vibration_limit=3
):
    """
    Prototype rule-based spoilage risk score.
    Default thresholds are demo assumptions, not
    scientifically validated limits.
    """

    risk_score = 0
    risk_factors = []

    # Temperature risk
    if temperature > temperature_limit:
        risk_score += 40
        risk_factors.append("High temperature")

    # Humidity risk
    if humidity > humidity_limit:
        risk_score += 35
        risk_factors.append("High humidity")

    # Vibration risk
    if vibration > vibration_limit:
        risk_score += 25
        risk_factors.append("High vibration")

    if risk_score <= 25:
        risk_level = "LOW"
    elif risk_score <= 60:
        risk_level = "MEDIUM"
    else:
        risk_level = "HIGH"

    return {
        "risk_score": risk_score,
        "risk_level": risk_level,
        "risk_factors": risk_factors
    }


if __name__ == "__main__":
    result = calculate_spoilage_risk(
        temperature=35,
        humidity=80,
        vibration=4.5
    )

    print("\nAtmoSync Spoilage Risk Analysis")
    print("Risk Score:", result["risk_score"])
    print("Risk Level:", result["risk_level"])
    print("Risk Factors:", result["risk_factors"])
