from backend.data.sample_complaints import SAMPLE_COMPLAINTS
from backend.services.incident_intelligence_service import (
    IncidentIntelligenceService,
)
from backend.services.incident_response_formatter import (
    IncidentResponseFormatter,
)


def test_frontend_ready_response():

    service = IncidentIntelligenceService()
    formatter = IncidentResponseFormatter()

    analysis = service.analyze(
        SAMPLE_COMPLAINTS
    )

    result = formatter.format(
        analysis
    )

    assert "total_complaints" in result
    assert "total_incidents" in result
    assert "incidents" in result

    assert result["total_complaints"] == 5

    assert len(
        result["incidents"]
    ) == result["total_incidents"]

    for incident in result["incidents"]:

        assert "incident_id" in incident
        assert "priority" in incident

        assert "risk" in incident
        assert "score" in incident["risk"]
        assert "severity" in incident["risk"]
        assert (
            "escalation_required"
            in incident["risk"]
        )

        assert "complaints" in incident
        assert "count" in incident["complaints"]
        assert "ids" in incident["complaints"]

        assert "location" in incident
        assert "hazards" in incident

        assert "correlation" in incident
        assert (
            "average_score"
            in incident["correlation"]
        )

        assert "risk_factors" in incident
        assert "explanation" in incident


def test_frontend_response_location_and_hazards():

    service = IncidentIntelligenceService()
    formatter = IncidentResponseFormatter()

    analysis = service.analyze(
        SAMPLE_COMPLAINTS
    )

    result = formatter.format(
        analysis
    )

    incidents = result["incidents"]

    assert len(incidents) > 0

    found_water_incident = False

    for incident in incidents:

        if "water_leak" in incident["hazards"]:

            found_water_incident = True

            assert (
                "A Block"
                in incident["location"]["hostels"]
            )

            assert (
                2
                in incident["location"]["floors"]
            )

    assert found_water_incident
