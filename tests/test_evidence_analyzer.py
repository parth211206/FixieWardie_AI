from PIL import Image

from backend.app.evidence_analyzer import EvidenceAnalyzer


def test_evidence_analyzer_with_image(tmp_path):

    image_path = tmp_path / "complaint.png"

    image = Image.new(
        "RGB",
        (800, 600)
    )

    image.save(image_path)

    analyzer = EvidenceAnalyzer()

    result = analyzer.analyze(
        str(image_path)
    )

    assert result["image_provided"] is True
    assert result["image_valid"] is True
    assert result["confidence"] == 0.50
    assert result["image_metadata"]["width"] == 800
    assert result["image_metadata"]["height"] == 600


def test_evidence_analyzer_without_image():

    analyzer = EvidenceAnalyzer()

    result = analyzer.analyze()

    assert result["image_provided"] is False
    assert result["image_valid"] is False
    assert result["confidence"] == 0.0