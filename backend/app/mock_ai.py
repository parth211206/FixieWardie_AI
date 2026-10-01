class MockAIClient:

    def analyze_complaint(self, description: str, category: str | None = None):

        text = description.lower()

        # Electrical hazard
        if (
            "spark" in text
            or "shock" in text
            or "wire" in text
            or "electrical" in text
            or "switchboard" in text
        ):
            return {
                "normalized_issue": description,
                "corrected_category": "Electrical Hazard",
                "category_overridden": category != "Electrical",
                "detected_hazards": [
                    "possible electrical hazard"
                ],
                "required_skill": "Electrical",
                "initial_severity": "High"
            }

        # Plumbing
        if (
            "leak" in text
            or "water" in text
            or "pipe" in text
            or "tap" in text
            or "faucet" in text
        ):
            return {
                "normalized_issue": description,
                "corrected_category": "Plumbing",
                "category_overridden": category != "Plumbing",
                "detected_hazards": [],
                "required_skill": "Plumber",
                "initial_severity": "Medium"
            }

        # HVAC
        if (
            "air conditioner" in text
            or "ac " in text
            or "ac is" in text
            or "cooling" in text
            or "fan" in text
        ):
            return {
                "normalized_issue": description,
                "corrected_category": "HVAC",
                "category_overridden": category != "HVAC",
                "detected_hazards": [],
                "required_skill": "HVAC Technician",
                "initial_severity": "Medium"
            }

        # Default
        return {
            "normalized_issue": description,
            "corrected_category": category or "General Maintenance",
            "category_overridden": False,
            "detected_hazards": [],
            "required_skill": "General Maintenance",
            "initial_severity": "Low"
        }

    def analyze_evidence(self, image_provided: bool):

        if not image_provided:
            return {
                "image_provided": False,
                "visible_conditions": [],
                "confidence": 0.0
            }

        # This is ONLY a development mock.
        return {
            "image_provided": True,
            "visible_conditions": [
                "image evidence available for inspection"
            ],
            "confidence": 0.50
        }