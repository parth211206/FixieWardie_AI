from .schemas import ComplaintInput
from .ai_client import ai_client
from .evidence_analyzer import EvidenceAnalyzer


class IntakeAgent:

    def __init__(self):
        self.evidence_analyzer = EvidenceAnalyzer()

    def analyze(
        self,
        complaint: ComplaintInput,
        image_path: str | None = None
    ):

        # Analyze the complaint using Gemini
        triage_data = ai_client.analyze_complaint(
            description=complaint.description,
            category=complaint.category,
            location=complaint.location
        )

        # Analyze image evidence
        evidence_data = self.evidence_analyzer.analyze(
            image_path=image_path
        )

        # Combine both results
        result = {
            "request_id": "REQ-001",

            "triage": {
                "original_category": complaint.category,
                **triage_data
            },

            "evidence": evidence_data
        }

        return result