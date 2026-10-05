import asyncio
from app.orchestrator import AgentContext, Orchestrator

def test_farming_weather_path_is_source_grounded():
    intent, reply, result = asyncio.run(Orchestrator().handle("कल बारिश होगी?", AgentContext(household_id="h1")))
    assert intent == "farming"
    assert result is not None and result.ok
    assert "बारिश" in reply
    assert result.source is not None
    assert "DEMO DATA" in (result.source.freshness_note or "")

def test_scheme_path_is_deterministic():
    intent, reply, _ = asyncio.run(Orchestrator().handle("मुझे किसान योजना बताओ", AgentContext(household_id="h1")))
    assert intent == "scheme"
    assert "योजनाओं" in reply

def test_explicit_human_path_is_safe():
    intent, reply, result = asyncio.run(Orchestrator().handle("मुझे किसी इंसान से बात करनी है", AgentContext(household_id="h1")))
    assert intent == "human"
    assert result is None
    assert "volunteer" in reply

def test_mandi_path_labels_demo_data():
    intent, reply, result = asyncio.run(Orchestrator().handle("सोनीपत मंडी में गेहूं का भाव", AgentContext(household_id="h1")))
    assert intent == "farming"
    assert result is not None and result.ok
    assert "डेमो" in reply
