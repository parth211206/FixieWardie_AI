from pydantic import BaseModel
from typing import List, Optional


class IncidentResult(BaseModel):

    incident_detected: bool

    incident_id: Optional[str] = None

    related_complaints: List[str] = []

    correlation_score: float = 0.0

    escalation_signal: bool = False
