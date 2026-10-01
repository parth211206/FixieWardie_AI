# ============================================================
# FixieWardie AI
# Member 2 - Risk Assessment Engine
# ============================================================

from typing import Dict, List, Any

from backend.data.risk_rules import (
    CATEGORY_SCORES,
    HAZARD_SCORES,
    COMBINATION_RULES,
)


class RiskEngine:
    """
    Deterministic risk assessment engine.

    The AI/LLM provides evidence.
    This engine converts that evidence into
    a transparent risk score.

    Output:
        score
        severity
        escalation_signal
        factors
    """

    def assess(self, complaint: Dict[str, Any]) -> Dict[str, Any]:

        score = 0

        factors: List[str] = []

        # ====================================================
        # 1. CATEGORY
        # ====================================================

        category = complaint.get(
            "category",
            "other"
        ).lower().strip()

        category_score = CATEGORY_SCORES.get(
            category,
            CATEGORY_SCORES["other"]
        )

        score += category_score

        if category_score > 10:

            factors.append({
                "type": "category",
                "description": (
                    f"{category.title()} complaint "
                    f"has a base risk score of {category_score}."
                ),
                "points": category_score
            })

        # ====================================================
        # 2. COLLECT HAZARDS
        # ====================================================

        text_analysis = complaint.get(
            "text_analysis",
            {}
        ) or {}

        image_analysis = complaint.get(
            "image_analysis",
            {}
        ) or {}

        text_hazards = set(
            h.lower().strip()
            for h in text_analysis.get(
                "hazards",
                []
            )
        )

        image_hazards = set(
            h.lower().strip()
            for h in image_analysis.get(
                "detected_hazards",
                []
            )
        )

        all_hazards = text_hazards | image_hazards

        # ====================================================
        # 3. HAZARD SCORES
        # ====================================================

        for hazard in all_hazards:

            if hazard not in HAZARD_SCORES:
                continue

            points = HAZARD_SCORES[hazard]

            # If both text and image independently detect
            # the same hazard, increase confidence slightly.
            detected_by_both = (
                hazard in text_hazards
                and hazard in image_hazards
            )

            if detected_by_both:

                points += 5

                factors.append({
                    "type": "hazard",
                    "description": (
                        f"{hazard.replace('_', ' ')} "
                        "detected by both text and image analysis."
                    ),
                    "points": points
                })

            else:

                source = (
                    "image"
                    if hazard in image_hazards
                    else "text"
                )

                factors.append({
                    "type": "hazard",
                    "description": (
                        f"{hazard.replace('_', ' ')} "
                        f"detected from {source} analysis."
                    ),
                    "points": points
                })

            score += points

        # ====================================================
        # 4. CONFIDENCE
        # ====================================================

        image_confidence = float(
            image_analysis.get(
                "confidence",
                0
            ) or 0
        )

        text_confidence = float(
            text_analysis.get(
                "confidence",
                0
            ) or 0
        )

        if image_confidence >= 0.90:

            score += 5

            factors.append({
                "type": "confidence",
                "description": "High-confidence image analysis.",
                "points": 5
            })

        elif image_confidence >= 0.75:

            score += 3

            factors.append({
                "type": "confidence",
                "description": "Moderate-confidence image analysis.",
                "points": 3
            })

        if text_confidence >= 0.90:

            score += 3

            factors.append({
                "type": "confidence",
                "description": "High-confidence text analysis.",
                "points": 3
            })

        # ====================================================
        # 5. COMBINATION RULES
        # ====================================================

        for rule in COMBINATION_RULES:

            required_hazards = rule["required"]

            if required_hazards.issubset(all_hazards):

                score += rule["bonus"]

                factors.append({
                    "type": "combination",
                    "description": rule["reason"],
                    "points": rule["bonus"]
                })

        # ====================================================
        # 6. CAP SCORE
        # ====================================================

        score = min(
            max(score, 0),
            100
        )

        # ====================================================
        # 7. SEVERITY
        # ====================================================

        if score <= 24:

            severity = "LOW"

        elif score <= 49:

            severity = "MEDIUM"

        elif score <= 74:

            severity = "HIGH"

        else:

            severity = "CRITICAL"

        # ====================================================
        # 8. ESCALATION
        # ====================================================

        escalation_signal = severity in [
            "HIGH",
            "CRITICAL"
        ]

        # ====================================================
        # 9. HUMAN READABLE EXPLANATION
        # ====================================================

        explanation = self._generate_explanation(
            severity,
            score,
            factors
        )

        return {
            "score": score,
            "severity": severity,
            "escalation_signal": escalation_signal,
            "factors": factors,
            "explanation": explanation
        }

    # ========================================================
    # EXPLANATION GENERATOR
    # ========================================================

    def _generate_explanation(
        self,
        severity: str,
        score: int,
        factors: List[Dict[str, Any]]
    ) -> str:

        if not factors:

            return (
                f"Risk score is {score}/100 with "
                f"{severity} severity."
            )

        important_factors = sorted(
            factors,
            key=lambda x: x["points"],
            reverse=True
        )[:3]

        reasons = [
            factor["description"]
            for factor in important_factors
        ]

        return (
            f"Risk score is {score}/100 ({severity}). "
            + " ".join(reasons)
        )