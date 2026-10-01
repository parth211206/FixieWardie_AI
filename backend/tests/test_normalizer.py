from backend.normalizers.complaint_normalizer import ComplaintNormalizer


def test_normalize_complaint():
    normalizer = ComplaintNormalizer()

    incoming = {
        "id": "CMP-101",
        "category": "Electrical",
        "text": "Sparks are coming from the wires.",
        "timestamp": "2026-10-01T20:00:00",
        "location": {
            "hostel": "A Block",
            "floor": 2,
            "room": 204,
        },
        "image_analysis": {
            "detected_hazards": ["sparks"],
            "confidence": 0.93,
        },
    }

    result = normalizer.normalize(incoming)

    assert result["complaint_id"] == "CMP-101"
    assert result["category"] == "electrical"
    assert result["description"] == "Sparks are coming from the wires."

    assert result["location"]["hostel"] == "A Block"
    assert result["location"]["floor"] == 2

    assert result["image_analysis"]["detected_hazards"] == ["sparks"]
    assert result["image_analysis"]["confidence"] == 0.93


def test_normalize_missing_analysis():
    normalizer = ComplaintNormalizer()

    incoming = {
        "complaint_id": "CMP-102",
        "description": "The bathroom needs cleaning.",
        "timestamp": "2026-10-01T20:10:00",
    }

    result = normalizer.normalize(incoming)

    assert result["complaint_id"] == "CMP-102"
    assert result["category"] == "other"
    assert result["text_analysis"]["hazards"] == []
    assert result["image_analysis"]["detected_hazards"] == []
    assert result["image_analysis"]["confidence"] == 0.0
