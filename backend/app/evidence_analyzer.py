import base64
import json

from .image_utils import validate_image
from .ai_client import client, GEMINI_MODEL


class EvidenceAnalyzer:

    def analyze(self, image_path: str | None = None):

        # No image was provided
        if image_path is None:
            return {
                "image_provided": False,
                "image_valid": False,
                "visible_conditions": [],
                "confidence": 0.0
            }

        # Validate the image using the existing image utility
        validation = validate_image(image_path)

        # Image exists but cannot be used
        if not validation["valid"]:
            return {
                "image_provided": True,
                "image_valid": False,
                "visible_conditions": [],
                "confidence": 0.0,
                "validation_error": validation["reason"]
            }

        # Read the validated image
        with open(image_path, "rb") as image_file:
            image_bytes = image_file.read()

        # Convert image to base64
        image_data = base64.b64encode(image_bytes).decode("utf-8")

        # Convert image format to MIME type
        mime_types = {
            "JPEG": "image/jpeg",
            "PNG": "image/png",
            "WEBP": "image/webp"
        }

        mime_type = mime_types[validation["format"]]

        prompt = """
You are the visual evidence analyzer for ARIA
(Agentic Risk Intelligence for Accommodation).

Inspect the uploaded maintenance complaint image.

Identify only conditions that are visibly supported by the image.

Focus on:
- water or liquid leakage
- electrical equipment or wiring
- visible sparks, burns, smoke or fire indicators
- damaged pipes, walls, ceilings or fixtures
- flooding or standing water
- physical damage
- other clearly visible maintenance hazards

Do not invent anything that cannot be seen.

Return ONLY valid JSON using exactly this structure:

{
    "visible_conditions": [],
    "confidence": 0.0
}

The confidence must be a number between 0.0 and 1.0.
"""

        interaction = client.interactions.create(
            model=GEMINI_MODEL,
            input=[
                {
                    "type": "text",
                    "text": prompt
                },
                {
                    "type": "image",
                    "data": image_data,
                    "mime_type": mime_type
                }
            ],
            response_format={
                "type": "text",
                "mime_type": "application/json",
                "schema": {
                    "type": "object",
                    "properties": {
                        "visible_conditions": {
                            "type": "array",
                            "items": {
                                "type": "string"
                            }
                        },
                        "confidence": {
                            "type": "number"
                        }
                    },
                    "required": [
                        "visible_conditions",
                        "confidence"
                    ]
                }
            }
        )

        result = json.loads(interaction.output_text)

        return {
            "image_provided": True,
            "image_valid": True,
            "visible_conditions": result["visible_conditions"],
            "confidence": result["confidence"],
            "image_metadata": {
                "format": validation["format"],
                "width": validation["width"],
                "height": validation["height"]
            }
        }