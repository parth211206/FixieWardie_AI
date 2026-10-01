from backend.engines.risk_engine import RiskEngine


class IncidentRiskEngine:
    """
    Calculates the overall risk of a clustered incident.

    The incident risk is derived from:
    - Individual complaint risk
    - Number of affected complaints
    - Highest severity
    - Combined hazards
    - Cross-complaint hazard confirmation
    """

    SEVERITY_RANK = {
        "LOW": 1,
        "MEDIUM": 2,
        "HIGH": 3,
        "CRITICAL": 4,
    }

    def __init__(self, risk_engine=None):
        self.risk_engine = risk_engine or RiskEngine()

    def assess_incident(self, incident):
        """
        Assess one incident cluster.

        Returns a new incident dictionary containing
        risk information.
        """

        complaints = incident.get("complaints", [])

        if not complaints:
            return {
                **incident,
                "risk_score": 0,
                "severity": "LOW",
                "escalation_signal": False,
                "risk_factors": [],
                "explanation": "No complaints in incident.",
            }

        complaint_assessments = []

        for complaint in complaints:
            assessment = self.risk_engine.assess(
                complaint
            )

            complaint_assessments.append(
                assessment
            )

        highest_score = max(
            assessment.get("score", 0)
            for assessment in complaint_assessments
        )

        highest_severity = max(
            complaint_assessments,
            key=lambda item: self.SEVERITY_RANK.get(
                item.get("severity", "LOW"),
                1,
            ),
        )

        average_score = (
            sum(
                assessment.get("score", 0)
                for assessment in complaint_assessments
            )
            / len(complaint_assessments)
        )

        complaint_count = len(complaints)

        # Start with the highest individual risk.
        incident_score = highest_score

        # Multiple complaints indicate a potentially wider incident.
        if complaint_count >= 2:
            incident_score += 5

        if complaint_count >= 3:
            incident_score += 5

        # Multiple complaints with the same hazard provide
        # additional evidence that the hazard is real.
        hazard_counts = {}

        for complaint in complaints:
            hazards = set()

            text_analysis = complaint.get(
                "text_analysis",
                {}
            )

            image_analysis = complaint.get(
                "image_analysis",
                {}
            )

            hazards.update(
                text_analysis.get("hazards", [])
            )

            hazards.update(
                image_analysis.get(
                    "detected_hazards",
                    []
                )
            )

            for hazard in hazards:
                hazard_counts[hazard] = (
                    hazard_counts.get(hazard, 0) + 1
                )

        repeated_hazards = [
            hazard
            for hazard, count in hazard_counts.items()
            if count >= 2
        ]

        if repeated_hazards:
            incident_score += min(
                len(repeated_hazards) * 5,
                15
            )

        incident_score = min(
            round(incident_score),
            100
        )

        severity = self._severity_from_score(
            incident_score
        )

        # Never downgrade an incident below the highest
        # individual complaint severity.
        if (
            self.SEVERITY_RANK.get(
                highest_severity.get("severity", "LOW"),
                1,
            )
            > self.SEVERITY_RANK.get(
                severity,
                1,
            )
        ):
            severity = highest_severity["severity"]

        escalation_signal = severity in {
            "HIGH",
            "CRITICAL",
        }

        risk_factors = []

        if complaint_count >= 2:
            risk_factors.append(
                f"{complaint_count} complaints linked to same incident"
            )

        if repeated_hazards:
            risk_factors.append(
                "Repeated hazards: "
                + ", ".join(sorted(repeated_hazards))
            )

        if highest_score >= 75:
            risk_factors.append(
                "At least one complaint has critical-level risk"
            )
        elif highest_score >= 50:
            risk_factors.append(
                "At least one complaint has high-level risk"
            )

        explanation = self._build_explanation(
            complaint_count,
            severity,
            average_score,
            repeated_hazards,
        )

        return {
            **incident,
            "risk_score": incident_score,
            "severity": severity,
            "escalation_signal": escalation_signal,
            "risk_factors": risk_factors,
            "explanation": explanation,
            "complaint_risks": complaint_assessments,
        }

    def assess_all(self, incidents):
        """
        Assess every incident in a list.
        """

        assessed = [
            self.assess_incident(incident)
            for incident in incidents
        ]

        return sorted(
            assessed,
            key=lambda incident: incident.get(
                "risk_score",
                0
            ),
            reverse=True,
        )

    def _severity_from_score(self, score):
        if score <= 24:
            return "LOW"

        if score <= 49:
            return "MEDIUM"

        if score <= 74:
            return "HIGH"

        return "CRITICAL"

    def _build_explanation(
        self,
        complaint_count,
        severity,
        average_score,
        repeated_hazards,
    ):
        explanation = (
            f"Incident contains {complaint_count} "
            f"linked complaint(s). "
            f"Average complaint risk is "
            f"{round(average_score, 1)}."
        )

        if repeated_hazards:
            explanation += (
                " Repeated hazards detected: "
                + ", ".join(sorted(repeated_hazards))
                + "."
            )

        explanation += (
            f" Overall incident severity: {severity}."
        )

        return explanation
