from backend.engines.incident_cluster_engine import (
    IncidentClusterEngine
)
from backend.data.sample_complaints import (
    SAMPLE_COMPLAINTS
)


def test_incident_clustering():

    engine = IncidentClusterEngine()

    clusters = engine.cluster(
        SAMPLE_COMPLAINTS
    )

    print()
    print("=" * 60)
    print("INCIDENT CLUSTER ENGINE TEST")
    print("=" * 60)

    for cluster in clusters:
        print()
        print(
            f"Incident: {cluster['incident_id']}"
        )

        print(
            f"Complaints: "
            f"{cluster['complaint_ids']}"
        )

        print(
            f"Size: {cluster['size']}"
        )

        print(
            f"Average correlation: "
            f"{cluster['average_correlation']}"
        )

        print(
            f"Scores: "
            f"{cluster['correlation_scores']}"
        )

    print()
    print("=" * 60)

    assert isinstance(clusters, list)
    assert len(clusters) > 0

    all_complaint_ids = []

    for cluster in clusters:
        all_complaint_ids.extend(
            cluster["complaint_ids"]
        )

    assert set(all_complaint_ids) == {
        complaint["complaint_id"]
        for complaint in SAMPLE_COMPLAINTS
    }
