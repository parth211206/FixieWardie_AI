from backend.engines.correlation_engine import CorrelationEngine


class IncidentClusterEngine:
    """
    Groups related complaints into possible incidents.

    Uses the CorrelationEngine to determine whether
    complaints are sufficiently related.
    """

    def __init__(self, correlation_engine=None):
        self.correlation_engine = (
            correlation_engine
            or CorrelationEngine()
        )

    def cluster(self, complaints):
        """
        Group complaints into incident clusters.

        Returns:
            [
                {
                    "incident_id": "INC-001",
                    "complaint_ids": [...],
                    "complaints": [...],
                    "correlation_scores": [...],
                    "average_correlation": ...,
                    "size": ...
                }
            ]
        """

        if not complaints:
            return []

        clusters = []
        assigned = set()

        for complaint in complaints:
            complaint_id = complaint.get("complaint_id")

            if complaint_id in assigned:
                continue

            cluster_complaints = [complaint]
            cluster_ids = {complaint_id}
            correlation_scores = []

            remaining = [
                item
                for item in complaints
                if item.get("complaint_id") != complaint_id
            ]

            related = self.correlation_engine.find_related(
                complaint,
                remaining
            )

            for result in related:
                related_id = result["complaint_b"]

                if related_id in assigned:
                    continue

                matching_complaint = next(
                    (
                        item
                        for item in remaining
                        if item.get("complaint_id")
                        == related_id
                    ),
                    None
                )

                if matching_complaint is None:
                    continue

                cluster_complaints.append(
                    matching_complaint
                )

                cluster_ids.add(related_id)

                correlation_scores.append(
                    result["correlation_score"]
                )

            assigned.update(cluster_ids)

            if correlation_scores:
                average_correlation = round(
                    sum(correlation_scores)
                    / len(correlation_scores),
                    4
                )
            else:
                average_correlation = 1.0

            clusters.append(
                {
                    "incident_id": (
                        f"INC-{len(clusters) + 1:03d}"
                    ),
                    "complaint_ids": list(
                        cluster_ids
                    ),
                    "complaints": cluster_complaints,
                    "correlation_scores": (
                        correlation_scores
                    ),
                    "average_correlation": (
                        average_correlation
                    ),
                    "size": len(cluster_complaints),
                }
            )

        return clusters
