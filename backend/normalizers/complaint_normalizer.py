from typing import Any

from .hazard_normalizer import normalize_hazards


class ComplaintNormalizer:
    """
    Converts incoming complaint payloads into the standard
    structure expected by the incident intelligence engines.
    """

    DEFAULT_CATEGORY = "other"

    def normalize(self, complaint: dict[str, Any]) -> dict[str, Any]:
        location = complaint.get("location") or {}

        text_analysis = complaint.get("text_analysis") or {}
        image_analysis = complaint.get("image_analysis") or {}

        normalized = {
            "complaint_id": str(
                complaint.get("complaint_id")
                or complaint.get("id")
                or ""
            ),

            "category": str(
                complaint.get("category")
                or self.DEFAULT_CATEGORY
            ).lower(),

            "description": str(
                complaint.get("description")
                or complaint.get("text")
                or ""
            ).strip(),

            "timestamp": str(
                complaint.get("timestamp")
                or ""
            ),

            "location": {
                "hostel": location.get("hostel"),
                "building": location.get("building"),
                "floor": location.get("floor"),
                "room": location.get("room"),
            },

            "text_analysis": {
                "hazards": normalize_hazards(
                    self._as_list(text_analysis.get("hazards"))
                ),
                "confidence": self._as_float(
                    text_analysis.get("confidence")
                ),
            },

            "image_analysis": {
                "detected_hazards": normalize_hazards(
                    self._as_list(
                        image_analysis.get("detected_hazards")
                    )
                ),
                "confidence": self._as_float(
                    image_analysis.get("confidence")
                ),
            },

            "image_url": complaint.get("image_url"),

            "metadata": complaint.get("metadata") or {},
        }

        return normalized

    @staticmethod
    def _as_list(value: Any) -> list[str]:
        if value is None:
            return []

        if isinstance(value, list):
            return [str(item).lower() for item in value]

        return [str(value).lower()]

    @staticmethod
    def _as_float(value: Any) -> float:
        try:
            if value is None:
                return 0.0

            return max(0.0, min(1.0, float(value)))

        except (TypeError, ValueError):
            return 0.0

    def normalize_many(
        self,
        complaints: list[dict[str, Any]],
    ) -> list[dict[str, Any]]:
        return [
            self.normalize(complaint)
            for complaint in complaints
        ]