from backend.services.incident_intelligence_service import (
    IncidentIntelligenceService
)

from backend.data.sample_complaints import (
    SAMPLE_COMPLAINTS
)


def test_incident_intelligence_service():

    service = IncidentIntelligenceService()

    result = service.analyze(
        SAMPLE_COMPLAINTS
    )

    print()
    print("=" * 70)
    print("INCIDENT INTELLIGENCE SERVICE")
    print("=" * 70)

    print()
    print(
        f"Total complaints: "
        f"{result['total_complaints']}"
    )

    print(
        f"Total incidents: "
        f"{result['total_incidents']}"
    )

    for incident in result["incidents"]:

        print()
        print("-" * 70)

        print(
            f"Priority: "
            f"{incident['priority']}"
        )

        print(
            f"Incident: "
            f"{incident['incident_id']}"
        )

        print(
            f"Complaints: "
            f"{incident['complaint_ids']}"
        )

        print(
            f"Risk score: "
            f"{incident['risk_score']}"
        )

        print(
            f"Severity: "
            f"{incident['severity']}"
        )

        print(
            f"Escalation: "
            f"{incident['escalation_signal']}"
        )

        print(
            f"Factors: "
            f"{incident['risk_factors']}"
        )

    print()
    print("=" * 70)

    assert result["total_complaints"] == len(
        SAMPLE_COMPLAINTS
    )

    assert result["total_incidents"] > 0

    assert len(
        result["incidents"]
    ) == result["total_incidents"]


def test_empty_complaints():

    service = IncidentIntelligenceService()

    result = service.analyze([])

    assert result == {
        "total_complaints": 0,
        "total_incidents": 0,
        "incidents": [],
    }
