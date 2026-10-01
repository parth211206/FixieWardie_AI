from typing import Any, Optional


class Complaint:
    """
    Standard complaint representation used by the
    FixieWardie incident intelligence layer.
    """

    def __init__(
        self,
        complaint_id: str,
        category: str,
        description: str,
        timestamp: str,
        location: Optional[dict[str, Any]] = None,
        text_analysis: Optional[dict[str, Any]] = None,
        image_analysis: Optional[dict[str, Any]] = None,
        image_url: Optional[str] = None,
        metadata: Optional[dict[str, Any]] = None,
    ):
        self.complaint_id = complaint_id
        self.category = category
        self.description = description
        self.timestamp = timestamp

        self.location = location or {}
        self.text_analysis = text_analysis or {}
        self.image_analysis = image_analysis or {}

        self.image_url = image_url
        self.metadata = metadata or {}

    def to_dict(self) -> dict[str, Any]:
        return {
            "complaint_id": self.complaint_id,
            "category": self.category,
            "description": self.description,
            "timestamp": self.timestamp,
            "location": self.location,
            "text_analysis": self.text_analysis,
            "image_analysis": self.image_analysis,
            "image_url": self.image_url,
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Complaint":
        return cls(
            complaint_id=str(data.get("complaint_id", "")),
            category=str(data.get("category", "other")),
            description=str(data.get("description", "")),
            timestamp=str(data.get("timestamp", "")),
            location=data.get("location") or {},
            text_analysis=data.get("text_analysis") or {},
            image_analysis=data.get("image_analysis") or {},
            image_url=data.get("image_url"),
            metadata=data.get("metadata") or {},
        )
