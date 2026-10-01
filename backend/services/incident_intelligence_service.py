from typing import Any

from backend.engines.incident_cluster_engine import IncidentClusterEngine
from backend.engines.incident_risk_engine import IncidentRiskEngine
from backend.normalizers.complaint_normalizer import ComplaintNormalizer


class IncidentIntelligenceService:

    def __init__(
        self,
        cluster_engine=None,
        risk_engine=None,
        normalizer=None,
    ):
        self.cluster_engine = (
            cluster_engine or IncidentClusterEngine()
        )

        self.risk_engine = (
            risk_engine or IncidentRiskEngine()
        )

        self.normalizer = (
            normalizer or ComplaintNormalizer()
        )

    def analyze(
        self,
        complaints: list[dict[str, Any]],
    ) -> dict[str, Any]:

        normalized_complaints = (
            self.normalizer.normalize_many(complaints)
        )

        if not normalized_complaints:
            return {
                "total_complaints": 0,
                "total_incidents": 0,
                "incidents": [],
            }

        clusters = self.cluster_engine.cluster(
            normalized_complaints
        )

        incidents = self.risk_engine.assess_all(
            clusters
        )

        for index, incident in enumerate(
            incidents,
            start=1,
        ):
            incident["priority"] = index

        return {
            "total_complaints": len(
                normalized_complaints
            ),
            "total_incidents": len(incidents),
            "incidents": incidents,
        }

    def analyze_single(
        self,
        complaint: dict[str, Any],
        historical_complaints: list[
            dict[str, Any]
        ],
    ) -> dict[str, Any]:

        all_complaints = [
            complaint,
            *historical_complaints,
        ]

        return self.analyze(all_complaints)
