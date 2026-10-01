"""
Converts natural-language hazards produced by the
Member 1 AI intake layer into canonical hazard names
used by the Member 2 risk engine.
"""


HAZARD_MAP = {
    # Water / electrical
    "water near electricity": "water_near_electricity",
    "water near electrical equipment": "water_near_electricity",
    "water near electrical switchboard": "water_near_electricity",

    # Electrical
    "electrical shock risk": "electric_shock",
    "electric shock risk": "electric_shock",
    "electrical shock": "electric_shock",
    "electric shock": "electric_shock",

    "short circuit risk": "short_circuit",
    "short circuit": "short_circuit",

    "exposed wires": "exposed_wires",
    "exposed wiring": "exposed_wires",

    "sparks": "sparks",

    # Water
    "water leak": "water_leak",
    "water leakage": "water_leak",
    "flooding": "flooding",

    # Fire
    "fire": "fire",
    "smoke": "smoke",
    "flames": "flames",
    "burning smell": "burning_smell",

    # Gas
    "gas leak": "gas_leak",
    "gas": "gas",
    "gas smell": "gas_smell",

    # Structural
    "structural crack": "structural_crack",
    "ceiling damage": "ceiling_damage",
    "ceiling collapse": "ceiling_collapse",
    "wall collapse": "wall_collapse",

    # General safety
    "broken glass": "broken_glass",
    "slippery floor": "slippery_floor",
    "sewage": "sewage",
    "blocked exit": "blocked_exit",
    "security breach": "security_breach",
}


def normalize_hazard(hazard: str) -> str | None:
    """
    Convert one AI-generated hazard description into
    a canonical risk-engine hazard name.

    Returns None when no safe mapping is known.
    """
    if not hazard:
        return None

    cleaned = (
        str(hazard)
        .strip()
        .lower()
    )

    return HAZARD_MAP.get(cleaned)


def normalize_hazards(hazards: list[str]) -> list[str]:
    """
    Convert a list of AI-generated hazards into
    canonical hazard names.

    Unknown hazards are ignored rather than guessed.
    """
    normalized = []

    for hazard in hazards:
        canonical = normalize_hazard(hazard)

        if canonical and canonical not in normalized:
            normalized.append(canonical)

    return normalized