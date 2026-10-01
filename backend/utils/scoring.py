def clamp(value: float, minimum: float = 0, maximum: float = 100):
    """
    Keep a numeric score inside a defined range.
    """
    return max(minimum, min(value, maximum))
