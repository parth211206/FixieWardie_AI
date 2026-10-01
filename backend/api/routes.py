from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from backend.services.incident_intelligence_service import (
    IncidentIntelligenceService,
)
from backend.services.incident_response_formatter import (
    IncidentResponseFormatter,
)


router = APIRouter(
    prefix="/api",
    tags=["Incident Intelligence"],
)

service = IncidentIntelligenceService()
formatter = IncidentResponseFormatter()


class AnalyzeRequest(BaseModel):
    complaints: list[dict[str, Any]] = Field(
        default_factory=list,
        description="List of complaint objects to analyze.",
    )


class AnalyzeSingleRequest(BaseModel):
    complaint: dict[str, Any]
    historical_complaints: list[dict[str, Any]] = Field(
        default_factory=list,
    )


@router.get("/health")
def health_check() -> dict[str, str]:
    return {
        "status": "ok",
        "service": "FixieWardie Incident Intelligence API",
    }


@router.post("/analyze")
def analyze_complaints(
    request: AnalyzeRequest,
) -> dict[str, Any]:

    if not request.complaints:
        raise HTTPException(
            status_code=400,
            detail="At least one complaint is required.",
        )

    analysis = service.analyze(
        request.complaints
    )

    return formatter.format(
        analysis
    )


@router.post("/analyze-single")
def analyze_single_complaint(
    request: AnalyzeSingleRequest,
) -> dict[str, Any]:

    if not request.complaint:
        raise HTTPException(
            status_code=400,
            detail="Complaint is required.",
        )

    analysis = service.analyze_single(
        request.complaint,
        request.historical_complaints,
    )

    return formatter.format(
        analysis
    )
