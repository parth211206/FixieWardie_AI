from datetime import datetime
import math
import re


class CorrelationEngine:
    """
    Finds complaints that may belong to the same incident.

    Correlation is based on:
    1. Semantic similarity
    2. Location similarity
    3. Category similarity
    4. Time proximity
    """

    SEMANTIC_WEIGHT = 0.45
    LOCATION_WEIGHT = 0.25
    CATEGORY_WEIGHT = 0.15
    TIME_WEIGHT = 0.15

    CORRELATION_THRESHOLD = 0.65
    MAX_TIME_WINDOW_MINUTES = 24 * 60

    RELATED_CATEGORY_GROUPS = [
        {"water", "plumbing"},
        {"electrical", "fire"},
        {"structural", "maintenance"},
        {"sanitation", "plumbing"},
        {"security", "fire"},
    ]

    def find_related(self, complaint, historical_complaints):
        """
        Compare one complaint against historical complaints.

        Returns only complaints whose correlation score is
        greater than or equal to CORRELATION_THRESHOLD.
        """

        results = []

        for historical in historical_complaints:
            if (
                historical.get("complaint_id")
                == complaint.get("complaint_id")
            ):
                continue

            comparison = self.compare(
                complaint,
                historical
            )

            if comparison["related"]:
                results.append(comparison)

        results.sort(
            key=lambda item: item["correlation_score"],
            reverse=True
        )

        return results

    def compare(self, complaint_a, complaint_b):
        """
        Calculate correlation between two complaints.
        """

        semantic_score = self._semantic_similarity(
            complaint_a,
            complaint_b
        )

        location_score = self._location_similarity(
            complaint_a,
            complaint_b
        )

        category_score = self._category_similarity(
            complaint_a,
            complaint_b
        )

        time_score = self._time_similarity(
            complaint_a,
            complaint_b
        )

        correlation_score = (
            semantic_score * self.SEMANTIC_WEIGHT
            + location_score * self.LOCATION_WEIGHT
            + category_score * self.CATEGORY_WEIGHT
            + time_score * self.TIME_WEIGHT
        )

        correlation_score = round(
            min(max(correlation_score, 0.0), 1.0),
            4
        )

        return {
            "complaint_a": complaint_a.get("complaint_id"),
            "complaint_b": complaint_b.get("complaint_id"),
            "semantic_score": round(semantic_score, 4),
            "location_score": round(location_score, 4),
            "category_score": round(category_score, 4),
            "time_score": round(time_score, 4),
            "correlation_score": correlation_score,
            "related": correlation_score >= self.CORRELATION_THRESHOLD,
        }

    # ========================================================
    # SEMANTIC SIMILARITY
    # ========================================================

    def _semantic_similarity(self, complaint_a, complaint_b):
        """
        Lightweight deterministic semantic similarity.

        Uses:
        - description token overlap
        - hazard overlap

        This is intentionally dependency-free for the prototype.
        A real embedding model can replace this later.
        """

        text_a = self._tokenize(
            complaint_a.get("description", "")
        )

        text_b = self._tokenize(
            complaint_b.get("description", "")
        )

        text_similarity = self._jaccard(
            text_a,
            text_b
        )

        hazards_a = self._get_hazards(complaint_a)
        hazards_b = self._get_hazards(complaint_b)

        hazard_similarity = self._jaccard(
            hazards_a,
            hazards_b
        )

        # Hazards are more meaningful than individual words.
        score = (
            text_similarity * 0.40
            + hazard_similarity * 0.60
        )

        return min(score, 1.0)

    # ========================================================
    # LOCATION SIMILARITY
    # ========================================================

    def _location_similarity(self, complaint_a, complaint_b):
        """
        Compare hostel, building, floor and room.
        """

        location_a = complaint_a.get("location", {})
        location_b = complaint_b.get("location", {})

        score = 0.0

        if (
            location_a.get("hostel")
            and location_a.get("hostel")
            == location_b.get("hostel")
        ):
            score += 0.35

        if (
            location_a.get("building")
            and location_a.get("building")
            == location_b.get("building")
        ):
            score += 0.20

        if (
            location_a.get("floor") is not None
            and location_a.get("floor")
            == location_b.get("floor")
        ):
            score += 0.30

        room_a = location_a.get("room")
        room_b = location_b.get("room")

        if room_a is not None and room_b is not None:
            if room_a == room_b:
                score += 0.15

        return min(score, 1.0)

    # ========================================================
    # CATEGORY SIMILARITY
    # ========================================================

    def _category_similarity(self, complaint_a, complaint_b):
        category_a = complaint_a.get("category")
        category_b = complaint_b.get("category")

        if not category_a or not category_b:
            return 0.0

        if category_a == category_b:
            return 1.0

        for group in self.RELATED_CATEGORY_GROUPS:
            if category_a in group and category_b in group:
                return 0.5

        return 0.0

    # ========================================================
    # TIME SIMILARITY
    # ========================================================

    def _time_similarity(self, complaint_a, complaint_b):
        timestamp_a = complaint_a.get("timestamp")
        timestamp_b = complaint_b.get("timestamp")

        if not timestamp_a or not timestamp_b:
            return 0.0

        try:
            time_a = datetime.fromisoformat(timestamp_a)
            time_b = datetime.fromisoformat(timestamp_b)
        except (ValueError, TypeError):
            return 0.0

        difference_minutes = abs(
            (time_a - time_b).total_seconds()
        ) / 60

        if difference_minutes > self.MAX_TIME_WINDOW_MINUTES:
            return 0.0

        # Exponential decay:
        # same time = 1.0
        # farther apart = progressively lower
        score = math.exp(
            -difference_minutes / 240
        )

        return min(max(score, 0.0), 1.0)

    # ========================================================
    # HAZARD HELPERS
    # ========================================================

    def _get_hazards(self, complaint):
        hazards = set()

        text_analysis = complaint.get(
            "text_analysis",
            {}
        )

        image_analysis = complaint.get(
            "image_analysis",
            {}
        )

        for hazard in text_analysis.get("hazards", []):
            hazards.add(str(hazard).lower())

        for hazard in image_analysis.get(
            "detected_hazards",
            []
        ):
            hazards.add(str(hazard).lower())

        return hazards

    # ========================================================
    # TEXT HELPERS
    # ========================================================

    def _tokenize(self, text):
        """
        Convert text into normalized word tokens.
        """

        if not text:
            return set()

        words = re.findall(
            r"[a-zA-Z0-9]+",
            text.lower()
        )

        # Remove common words that don't help correlation.
        stop_words = {
            "the",
            "is",
            "a",
            "an",
            "from",
            "to",
            "and",
            "of",
            "in",
            "near",
            "has",
            "are",
            "on",
            "with",
        }

        return {
            word
            for word in words
            if word not in stop_words
        }

    def _jaccard(self, set_a, set_b):
        """
        Jaccard similarity:

        intersection / union
        """

        if not set_a and not set_b:
            return 1.0

        if not set_a or not set_b:
            return 0.0

        intersection = len(
            set_a.intersection(set_b)
        )

        union = len(
            set_a.union(set_b)
        )

        if union == 0:
            return 0.0

        return intersection / union
