from app.evaluation import run_intent_benchmark

def test_intent_benchmark():
    result = run_intent_benchmark()
    assert result["accuracy"] >= 0.8
