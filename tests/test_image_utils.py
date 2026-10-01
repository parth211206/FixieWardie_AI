from PIL import Image

from backend.app.image_utils import validate_image


def test_valid_image(tmp_path):

    image_path = tmp_path / "test.png"

    image = Image.new(
        "RGB",
        (500, 500)
    )

    image.save(image_path)

    result = validate_image(str(image_path))

    assert result["valid"] is True
    assert result["format"] == "PNG"
    assert result["width"] == 500
    assert result["height"] == 500


def test_small_image(tmp_path):

    image_path = tmp_path / "small.png"

    image = Image.new(
        "RGB",
        (50, 50)
    )

    image.save(image_path)

    result = validate_image(str(image_path))

    assert result["valid"] is False