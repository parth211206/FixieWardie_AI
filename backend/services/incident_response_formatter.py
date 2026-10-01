from typing import Any


class IncidentResponseFormatter:
    """
    Converts internal incident intelligence results into a
    stable frontend-friendly response format.
    """

    def format(
        self,
        analysis: dict[str, Any],
    ) -> dict[str, Any]:

        formatted_incidents = []

        for incident in analysis.get("incidents", []):
            formatted_incidents.append(
                self._format_incident(incident)
            )

        return {
            "total_complaints": analysis.get(
                "total_complaints",
                0,
            ),
            "total_incidents": analysis.get(
                "total_incidents",
                0,
            ),
            "incidents": formatted_incidents,
        }

    def _format_incident(
        self,
        incident: dict[str, Any],
    ) -> dict[str, Any]:

        complaints = incident.get("complaints", [])

        locations = self._extract_locations(
            complaints
        )

        hazards = self._extract_hazards(
            complaints
        )

        complaint_ids = incident.get(
            "complaint_ids",
            [],
        )

        return {
            "incident_id": incident.get(
                "incident_id"
            ),

            "priority": incident.get(
                "priority"
            ),

            "risk": {
                "score": incident.get(
                    "risk_score",
                    0,
                ),
                "severity": incident.get(
                    "severity",
                    "LOW",
                ),
                "escalation_required": incident.get(
                    "escalation_signal",
                    False,
                ),
            },

            "complaints": {
                "count": len(complaint_ids),
                "ids": complaint_ids,
            },

            "location": locations,

            "hazards": hazards,

            "correlation": {
                "average_score": incident.get(
                    "average_correlation",
                    0,
                ),
            },

            "risk_factors": incident.get(
                "risk_factors",
                [],
            ),

            "explanation": incident.get(
                "explanation",
                "",
            ),

            "complaint_risks": incident.get(
                "complaint_risks",
                [],
            ),
        }

    @staticmethod
    def _extract_locations(
        complaints: list[dict[str, Any]],
    ) -> dict[str, Any]:

        if not complaints:
            return {}

        hostel_values = []
        building_values = []
        floor_values = []
        room_values = []

        for complaint in complaints:
            location = complaint.get(
                "location",
                {},
            )

            if not location:
                continue

            if location.get("hostel") is not None:
                hostel_values.append(
                    location["hostel"]
                )

            if location.get("building") is not None:
                building_values.append(
                    location["building"]
                )

            if location.get("floor") is not None:
                floor_values.append(
                    location["floor"]
                )

            if location.get("room") is not None:
                room_values.append(
                    location["room"]
                )

        return {
            "hostels": list(
                dict.fromkeys(hostel_values)
            ),
            "buildings": list(
                dict.fromkeys(building_values)
            ),
            "floors": list(
                dict.fromkeys(floor_values)
            ),
            "rooms": list(
                dict.fromkeys(room_values)
            ),
        }

    @staticmethod
    def _extract_hazards(
        complaints: list[dict[str, Any]],
    ) -> list[str]:

        hazards = []

        for complaint in complaints:

            text_analysis = complaint.get(
                "text_analysis",
                {},
            )

            image_analysis = complaint.get(
                "image_analysis",
                {},
            )

            for hazard in text_analysis.get(
                "hazards",
                [],
            ):
                hazards.append(str(hazard))

            for hazard in image_analysis.get(
                "detected_hazards",
                [],
            ):
                hazards.append(str(hazard))

        return list(
            dict.fromkeys(hazards)
        )
