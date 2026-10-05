import asyncio

from app.orchestrator import AgentContext, Orchestrator
from app.schemas import LocationContext


def test_farming_weather_path_is_source_grounded():
    outcome = asyncio.run(Orchestrator().handle("कल बारिश होगी?", AgentContext(household_id="h1")))
    assert outcome.intent == "farming"
    assert outcome.result is not None and outcome.result.ok
    assert "बारिश" in outcome.reply
    assert outcome.result.source is not None
    assert "DEMO DATA" in (outcome.result.source.freshness_note or "")


def test_weather_uses_explicit_location_context():
    outcome = asyncio.run(Orchestrator().handle("कल बारिश होगी?", AgentContext(household_id="h1", location=LocationContext(latitude=28.61, longitude=77.21, label="Delhi"))))
    assert outcome.intent == "farming"
    assert outcome.result is not None and outcome.result.ok
    assert outcome.result.data["latitude"] == 28.61
    assert outcome.result.data["longitude"] == 77.21


def test_scheme_path_is_deterministic():
    outcome = asyncio.run(Orchestrator().handle("मुझे किसान योजना बताओ", AgentContext(household_id="h1")))
    assert outcome.intent == "scheme"
    assert "योजनाओं" in outcome.reply
    assert outcome.escalated is False


def test_explicit_human_path_uses_policy():
    outcome = asyncio.run(Orchestrator().handle("मुझे किसी इंसान से बात करनी है", AgentContext(household_id="h1")))
    assert outcome.intent == "human"
    assert outcome.result is None
    assert outcome.escalated is True
    assert outcome.escalation_reason == "explicit_human_request"


def test_mandi_path_labels_demo_data():
    outcome = asyncio.run(Orchestrator().handle("सोनीपत मंडी में गेहूं का भाव", AgentContext(household_id="h1")))
    assert outcome.intent == "farming"
    assert outcome.result is not None and outcome.result.ok
    assert "डेमो" in outcome.reply
