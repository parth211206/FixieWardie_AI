from pydantic import BaseModel
from typing import List


class RiskResult(BaseModel):

    score: float

    severity: str

    escalation_signal: bool

    factors: List[str]
