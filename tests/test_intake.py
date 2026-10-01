from PIL import Image

from backend.app.intake_agent import IntakeAgent
from backend.app.schemas import ComplaintInput


def test_plumbing_complaint():

    complaint = ComplaintInput(
        description="Water is leaking from the ceiling",
        category="Plumbing",
        location="Block A, Floor 2"
    )

    agent = IntakeAgent()

    result = agent.analyze(
        complaint
    )

    assert result["triage"]["corrected_category"] == "Plumbing"
    assert result["triage"]["required_skill"] == "Plumber"
    assert result["triage"]["initial_severity"] == "Medium"
    assert result["evidence"]["image_provided"] is False


def test_electrical_hazard_with_image(tmp_path):

    image_path = tmp_path / "electrical.png"

    image = Image.new(
        "RGB",
        (800, 600)
    )

    image.save(image_path)

    complaint = ComplaintInput(
        description="Water is leaking near the electrical switchboard",
        category="Plumbing",
        location="Block A, Floor 2"
    )

    agent = IntakeAgent()

    result = agent.analyze(
        complaint,
        image_path=str(image_path)
    )

    assert result["triage"]["corrected_category"] == "Electrical Hazard"
    assert result["triage"]["required_skill"] == "Electrical"
    assert result["triage"]["initial_severity"] == "High"
    assert result["triage"]["category_overridden"] is True

    assert result["evidence"]["image_provided"] is True
    assert result["evidence"]["image_valid"] is True