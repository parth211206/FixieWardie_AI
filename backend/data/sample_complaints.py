# ============================================================
# FixieWardie AI
# Member 2 - Sample Complaint Dataset
# ============================================================

SAMPLE_COMPLAINTS = [

    {
        "complaint_id": "CMP-001",

        "category": "water",

        "description": (
            "Water is leaking from the ceiling "
            "outside room 201."
        ),

        "timestamp": "2026-10-01T18:00:00",

        "location": {
            "hostel": "A Block",
            "building": "A",
            "floor": 2,
            "room": "201"
        },

        "text_analysis": {
            "hazards": [
                "water_leak"
            ],
            "confidence": 0.92
        },

        "image_analysis": {
            "detected_hazards": [
                "water_leak"
            ],
            "confidence": 0.90
        }
    },


    {
        "complaint_id": "CMP-002",

        "category": "plumbing",

        "description": (
            "Ceiling is dripping heavily "
            "near room 203."
        ),

        "timestamp": "2026-10-01T18:15:00",

        "location": {
            "hostel": "A Block",
            "building": "A",
            "floor": 2,
            "room": "203"
        },

        "text_analysis": {
            "hazards": [
                "water_leak"
            ],
            "confidence": 0.88
        },

        "image_analysis": {
            "detected_hazards": [
                "water_leak"
            ],
            "confidence": 0.91
        }
    },


    {
        "complaint_id": "CMP-003",

        "category": "electrical",

        "description": (
            "Water has reached the electrical "
            "panel in the second floor corridor."
        ),

        "timestamp": "2026-10-01T18:20:00",

        "location": {
            "hostel": "A Block",
            "building": "A",
            "floor": 2,
            "room": None
        },

        "text_analysis": {
            "hazards": [
                "water_near_electricity"
            ],
            "confidence": 0.95
        },

        "image_analysis": {
            "detected_hazards": [
                "water_near_electricity"
            ],
            "confidence": 0.96
        }
    },


    {
        "complaint_id": "CMP-004",

        "category": "electrical",

        "description": (
            "Sparks are coming from exposed "
            "wires near room 204."
        ),

        "timestamp": "2026-10-01T18:25:00",

        "location": {
            "hostel": "A Block",
            "building": "A",
            "floor": 2,
            "room": "204"
        },

        "text_analysis": {
            "hazards": [
                "sparks",
                "exposed_wires"
            ],
            "confidence": 0.95
        },

        "image_analysis": {
            "detected_hazards": [
                "sparks",
                "exposed_wires"
            ],
            "confidence": 0.97
        }
    },


    {
        "complaint_id": "CMP-005",

        "category": "sanitation",

        "description": (
            "Bathroom floor is dirty and "
            "needs cleaning."
        ),

        "timestamp": "2026-10-01T12:00:00",

        "location": {
            "hostel": "C Block",
            "building": "C",
            "floor": 1,
            "room": "101"
        },

        "text_analysis": {
            "hazards": [],
            "confidence": 0.90
        },

        "image_analysis": {
            "detected_hazards": [],
            "confidence": 0.85
        }
    }
]