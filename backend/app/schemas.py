from pydantic import BaseModel
from typing import List, Optional


class ComplaintInput(BaseModel):
    description: str
    category: Optional[str] = None
    location: Optional[str] = None


class TriageResult(BaseModel):
    original_category: Optional[str] = None
    normalized_issue: str
    corrected_category: str
    category_overridden: bool
    detected_hazards: List[str]
    required_skill: str
    initial_severity: str


class EvidenceResult(BaseModel):
    image_provided: bool
    visible_conditions: List[str]
    confidence: float


class IntakeResult(BaseModel):
    request_id: str
    triage: TriageResult
    evidence: EvidenceResult