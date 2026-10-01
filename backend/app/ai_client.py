import json
import os
import time

from dotenv import load_dotenv
from google import genai


# ============================================================
# LOAD ENVIRONMENT VARIABLES
# ============================================================

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise RuntimeError(
        "GEMINI_API_KEY not found. "
        "Make sure your .env file contains "
        "GEMINI_API_KEY=your_key"
    )


# ============================================================
# GEMINI CLIENT
# ============================================================

client = genai.Client(api_key=GEMINI_API_KEY)

GEMINI_MODEL = "gemini-3.5-flash-lite"


# ============================================================
# GEMINI AI CLIENT
# ============================================================

class GeminiAIClient:

    def analyze_complaint(
        self,
        description: str,
        category: str | None = None,
        location: str | None = None
    ):

        prompt = f"""
You are the complaint triage AI for ARIA
(Agentic Risk Intelligence for Accommodation).

Analyze a campus hostel maintenance complaint.

The student may have selected an incorrect category.
Use the actual description to determine the likely
maintenance issue.

STUDENT SELECTED CATEGORY:
{category or "Not provided"}

COMPLAINT:
{description}

LOCATION:
{location or "Not provided"}

Determine:

1. normalized_issue
   - Briefly describe what the actual issue appears to be.

2. corrected_category
   - Correct maintenance category.

3. category_overridden
   - true if the student's selected category is different
     from the corrected category.
   - false otherwise.

4. detected_hazards
   - List safety hazards supported by the complaint.
   - Use [] if there is no clear hazard.

5. required_skill
   - The type of technician expertise required.
   - Examples:
     Electrical
     Plumber
     HVAC Technician
     Structural Technician
     Fire Safety
     General Maintenance

6. initial_severity
   - One of:
     Low
     Medium
     High
     Critical

IMPORTANT:
- Do not select a specific technician.
- Do not invent facts.
- Do not assume a hazard without supporting evidence.
- This is an initial AI triage recommendation and not a
  professional safety inspection.

Return ONLY valid JSON using exactly this structure:

{{
    "normalized_issue": "",
    "corrected_category": "",
    "category_overridden": false,
    "detected_hazards": [],
    "required_skill": "",
    "initial_severity": ""
}}
"""

        interaction = client.interactions.create(
            model=GEMINI_MODEL,
            input=prompt,
            response_format={
                "type": "text",
                "mime_type": "application/json",
                "schema": {
                    "type": "object",
                    "properties": {
                        "normalized_issue": {
                            "type": "string"
                        },
                        "corrected_category": {
                            "type": "string"
                        },
                        "category_overridden": {
                            "type": "boolean"
                        },
                        "detected_hazards": {
                            "type": "array",
                            "items": {
                                "type": "string"
                            }
                        },
                        "required_skill": {
                            "type": "string"
                        },
                        "initial_severity": {
                            "type": "string"
                        }
                    },
                    "required": [
                        "normalized_issue",
                        "corrected_category",
                        "category_overridden",
                        "detected_hazards",
                        "required_skill",
                        "initial_severity"
                    ]
                }
            }
        )

        result = self._parse_json(
            interaction.output_text
        )

        return result


    @staticmethod
    def _parse_json(text: str) -> dict:

        text = text.strip()

        if text.startswith("```"):

            lines = text.splitlines()

            if lines:
                lines = lines[1:]

            if lines and lines[-1].strip() == "```":
                lines = lines[:-1]

            text = "\n".join(lines).strip()

        try:
            return json.loads(text)

        except json.JSONDecodeError as exc:
            raise ValueError(
                f"Gemini returned invalid JSON:\n{text}"
            ) from exc


# ============================================================
# SHARED CLIENT INSTANCE
# ============================================================

ai_client = GeminiAIClient()