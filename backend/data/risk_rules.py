# ============================================================
# FixieWardie AI
# Member 2 - Risk Rules
# ============================================================

CATEGORY_SCORES = {
    "electrical": 35,
    "fire": 70,
    "gas": 70,
    "structural": 55,
    "water": 25,
    "plumbing": 20,
    "sanitation": 15,
    "security": 40,
    "hvac": 20,
    "other": 10,
}


HAZARD_SCORES = {
    # Electrical
    "exposed_wires": 25,
    "sparks": 30,
    "electrical_fire": 35,
    "burn_damage": 20,
    "short_circuit": 30,
    "electric_shock": 35,

    # Fire
    "fire": 40,
    "smoke": 30,
    "flames": 45,
    "burning_smell": 25,

    # Gas
    "gas_leak": 40,
    "gas": 30,
    "gas_smell": 35,

    # Water
    "flooding": 25,
    "water_leak": 20,
    "water_near_electricity": 35,

    # Structural
    "structural_crack": 30,
    "ceiling_damage": 25,
    "ceiling_collapse": 40,
    "wall_collapse": 40,

    # General safety
    "broken_glass": 15,
    "slippery_floor": 10,
    "sewage": 20,
    "blocked_exit": 35,
    "security_breach": 25,
}


# ------------------------------------------------------------
# COMBINATION RULES
# ------------------------------------------------------------

COMBINATION_RULES = [

    {
        "name": "water_electrical",
        "required": {
            "water_leak",
            "exposed_wires"
        },
        "bonus": 25,
        "reason": "Water and exposed electrical wiring create a combined electrical hazard."
    },

    {
        "name": "water_electrical_2",
        "required": {
            "flooding",
            "electric_shock"
        },
        "bonus": 30,
        "reason": "Flooding combined with electrical shock creates an immediate safety hazard."
    },

    {
        "name": "sparks_electrical",
        "required": {
            "sparks",
            "exposed_wires"
        },
        "bonus": 20,
        "reason": "Sparks and exposed wiring indicate a potential electrical fire hazard."
    },

    {
        "name": "fire_smoke",
        "required": {
            "fire",
            "smoke"
        },
        "bonus": 20,
        "reason": "Fire and smoke detected together indicate an active fire-related hazard."
    },

    {
        "name": "gas_fire",
        "required": {
            "gas_leak",
            "fire"
        },
        "bonus": 30,
        "reason": "Gas leakage combined with fire creates a severe safety hazard."
    },

    {
        "name": "blocked_exit_fire",
        "required": {
            "blocked_exit",
            "fire"
        },
        "bonus": 30,
        "reason": "A blocked exit during a fire creates an evacuation risk."
    },

    {
        "name": "structural_collapse",
        "required": {
            "structural_crack",
            "ceiling_collapse"
        },
        "bonus": 25,
        "reason": "Structural damage combined with collapse evidence indicates a serious building safety risk."
    },
]