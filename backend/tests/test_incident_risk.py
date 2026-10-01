from backend.engines.incident_cluster_engine import (
    IncidentClusterEngine
)

from backend.engines.incident_risk_engine import (
    IncidentRiskEngine
)

from backend.data.sample_complaints import (
    SAMPLE_COMPLAINTS
)


def test_incident_risk():

    cluster_engine = IncidentClusterEngine()

    incidents = cluster_engine.cluster(
        SAMPLE_COMPLAINTS
    )

    risk_engine = IncidentRiskEngine()

    assessed_incidents = risk_engine.assess_all(
        incidents
    )

    print()
    print("=" * 60)
    print("INCIDENT RISK ENGINE TEST")
    print("=" * 60)

    for incident in assessed_incidents:

        print()
        print(
            f"Incident: {incident['incident_id']}"
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
            f"Risk factors: "
            f"{incident['risk_factors']}"
        )

        print(
            f"Explanation: "
            f"{incident['explanation']}"
        )

    print()
    print("=" * 60)

    assert isinstance(
        assessed_incidents,
        list
    )

    assert len(assessed_incidents) > 0

    for incident in assessed_incidents:

        assert 0 <= incident["risk_score"] <= 100

        assert incident["severity"] in {
            "LOW",
            "MEDIUM",
            "HIGH",
            "CRITICAL",
        }

        assert isinstance(
            incident["escalation_signal"],
            bool
        )
