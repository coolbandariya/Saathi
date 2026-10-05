from app.evaluation import CASES, run_intent_benchmark


def test_intent_benchmark_has_120_cases():
    assert len(CASES) == 120
    result = run_intent_benchmark()
    assert result["total"] == 120
    assert result["accuracy"] >= 0.95
