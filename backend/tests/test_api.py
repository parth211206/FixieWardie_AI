from fastapi.testclient import TestClient

from backend.main import app


client = TestClient(app)


def test_root():
    response = client.get("/")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "running"


def test_health():
    response = client.get("/api/health")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "ok"


def test_analyze():
    complaints = [
        {
            "complaint_id": "CMP-001",
            "category": "water",
            "description": (
                "Water is leaking from the ceiling "
                "outside room 201."
            ),
            "timestamp": "2026-10-01T18:00:00",
            "location": {
                "hostel": "A Block",
                "building": "A",
                "floor": 2,
                "room": "201",
            },
            "text_analysis": {
                "hazards": ["water_leak"],
                "confidence": 0.92,
            },
            "image_analysis": {
                "detected_hazards": ["water_leak"],
                "confidence": 0.88,
            },
        },
        {
            "complaint_id": "CMP-002",
            "category": "plumbing",
            "description": (
                "Ceiling is dripping heavily "
                "near room 203."
            ),
            "timestamp": "2026-10-01T18:15:00",
            "location": {
                "hostel": "A Block",
                "building": "A",
                "floor": 2,
                "room": "203",
            },
            "text_analysis": {
                "hazards": ["water_leak"],
                "confidence": 0.90,
            },
            "image_analysis": {
                "detected_hazards": ["water_leak"],
                "confidence": 0.86,
            },
        },
        {
            "complaint_id": "CMP-004",
            "category": "electrical",
            "description": (
                "Sparks are coming from exposed "
                "wires near room 204."
            ),
            "timestamp": "2026-10-01T18:25:00",
            "location": {
                "hostel": "A Block",
                "building": "A",
                "floor": 2,
                "room": "204",
            },
            "text_analysis": {
                "hazards": [
                    "sparks",
                    "exposed_wires",
                ],
                "confidence": 0.97,
            },
            "image_analysis": {
                "detected_hazards": [
                    "sparks",
                    "exposed_wires",
                ],
                "confidence": 0.95,
            },
        },
    ]

    response = client.post(
        "/api/analyze",
        json={"complaints": complaints},
    )

    assert response.status_code == 200

    data = response.json()

    assert data["total_complaints"] == 3
    assert data["total_incidents"] >= 1
    assert "incidents" in data

    for incident in data["incidents"]:

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


def test_analyze_empty():
    response = client.post(
        "/api/analyze",
        json={"complaints": []},
    )

    assert response.status_code == 400
