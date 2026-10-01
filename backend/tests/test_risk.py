from backend.engines.risk_engine import RiskEngine


def test_critical_electrical_complaint():

    engine = RiskEngine()

    complaint = {
        "complaint_id": "CMP-1024",

        "category": "electrical",

        "description": (
            "Sparks are coming from the switchboard "
            "near room 204."
        ),

        "text_analysis": {
            "hazards": [
                "electrical_fire"
            ],
            "confidence": 0.91,
        },

        "image_analysis": {
            "detected_hazards": [
                "exposed_wires",
                "sparks"
            ],
            "confidence": 0.94,
        },
    }

    result = engine.assess(complaint)

    print("\n========== RISK ASSESSMENT ==========")

    print(
        f"Risk Score: {result['score']}/100"
    )

    print(
        f"Severity: {result['severity']}"
    )

    print(
        f"Escalation: {result['escalation_signal']}"
    )

    print("\nRisk Factors:")

    for factor in result["factors"]:
        print(f" - {factor}")

    assert result["score"] > 0
    assert result["severity"] in [
        "LOW",
        "MEDIUM",
        "HIGH",
        "CRITICAL"
    ]


if __name__ == "__main__":
    test_critical_electrical_complaint()
