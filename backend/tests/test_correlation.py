from backend.engines.correlation_engine import CorrelationEngine
from backend.data.sample_complaints import SAMPLE_COMPLAINTS


def test_correlation():
    engine = CorrelationEngine()

    complaint = SAMPLE_COMPLAINTS[0]
    historical = SAMPLE_COMPLAINTS[1:]

    results = engine.find_related(
        complaint,
        historical
    )

    print()
    print("=" * 60)
    print("CORRELATION ENGINE TEST")
    print("=" * 60)

    for result in results:
        print()
        print(f"{result['complaint_a']} <-> {result['complaint_b']}")
        print(f"Semantic:   {result['semantic_score']}")
        print(f"Location:   {result['location_score']}")
        print(f"Category:   {result['category_score']}")
        print(f"Time:       {result['time_score']}")
        print(f"TOTAL:      {result['correlation_score']}")
        print(f"Related:    {result['related']}")

    print()
    print("=" * 60)

    assert isinstance(results, list)
    assert len(results) > 0
