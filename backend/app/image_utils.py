from PIL import Image


SUPPORTED_FORMATS = {
    "JPEG",
    "PNG",
    "WEBP"
}


def validate_image(image_path: str):

    try:
        with Image.open(image_path) as image:

            image_format = image.format
            width, height = image.size

            if image_format not in SUPPORTED_FORMATS:
                return {
                    "valid": False,
                    "reason": f"Unsupported image format: {image_format}"
                }

            if width < 100 or height < 100:
                return {
                    "valid": False,
                    "reason": "Image resolution is too small"
                }

            return {
                "valid": True,
                "format": image_format,
                "width": width,
                "height": height
            }

    except Exception as e:

        return {
            "valid": False,
            "reason": f"Unable to read image: {str(e)}"
        }