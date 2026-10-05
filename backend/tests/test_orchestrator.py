import asyncio
from app.orchestrator import AgentContext, Orchestrator

def test_farming_weather_path_is_source_grounded():
    intent, reply, result = asyncio.run(Orchestrator().handle("कल बारिश होगी?", AgentContext(household_id="h1")))
    assert intent == "farming"
    assert result is not None and result.ok
    assert "बारिश" in reply

def test_scheme_path_is_deterministic():
    intent, reply, _ = asyncio.run(Orchestrator().handle("मुझे किसान योजना बताओ", AgentContext(household_id="h1")))
    assert intent == "scheme"
    assert "योजनाओं" in reply
