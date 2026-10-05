import asyncio

from app.orchestrator import AgentContext, Orchestrator
from app.schemas import LocationContext


def test_farming_weather_requires_explicit_location():
    outcome = asyncio.run(Orchestrator().handle("कल बारिश होगी?", AgentContext(household_id="h1")))
    assert outcome.intent == "farming"
    assert outcome.result is None
    assert "स्थान" in outcome.reply


def test_weather_uses_explicit_location_context():
    outcome = asyncio.run(Orchestrator().handle("कल बारिश होगी?", AgentContext(household_id="h1", location=LocationContext(latitude=28.61, longitude=77.21, label="Delhi"))))
    assert outcome.intent == "farming"
    assert outcome.result is not None and outcome.result.ok
    assert outcome.result.data["latitude"] == 28.61
    assert outcome.result.data["longitude"] == 77.21


def test_scheme_path_is_deterministic():
    outcome = asyncio.run(Orchestrator().handle("मुझे किसान योजना बताओ", AgentContext(household_id="h1")))
    assert outcome.intent == "scheme"
    assert "PM-KISAN" in outcome.reply
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
    assert outcome.result.source is not None
    assert "DEMO DATA" in (outcome.result.source.freshness_note or "")


def test_mandi_without_live_configuration_is_not_presented_as_live(monkeypatch):
    from app import orchestrator as module
    class FakeSettings:
        demo_mode = False
        mandi_api_key = None
        mandi_resource_id = None
    monkeypatch.setattr(module, "get_settings", lambda: FakeSettings())
    instance = module.Orchestrator()
    assert instance.mandi is None


def test_mandi_requires_entities_instead_of_using_demo_defaults():
    outcome = asyncio.run(Orchestrator().handle("मंडी का आज का भाव बताओ", AgentContext(household_id="h1")))
    assert outcome.intent == "farming"
    assert outcome.result is None
    assert "फसल" in outcome.reply


def test_farmer_scheme_uses_official_pmkisan_source():
    outcome = asyncio.run(Orchestrator().handle("मुझे किसान योजना बताओ", AgentContext(household_id="h1")))
    assert outcome.intent == "scheme"
    assert outcome.result is not None and outcome.result.ok
    assert outcome.result.source is not None
    assert "pmkisan.gov.in" in outcome.result.source.url
    assert outcome.tool_name == "get_pmkisan_info"


def test_combined_mandi_and_weather_returns_both_evidence_paths():
    outcome = asyncio.run(Orchestrator().handle(
        "सोनीपत में गेहूं का मंडी भाव और अगले 24 घंटे में बारिश का chance?",
        AgentContext(
            household_id="h1",
            location=LocationContext(latitude=28.9931, longitude=77.0151, label="Sonipat"),
        ),
    ))
    assert outcome.intent == "farming"
    assert outcome.tool_name == "get_mandi_price+get_weather"
    assert len(outcome.results) == 2
    assert all(result.source is not None for result in outcome.results)
    assert "मॉडल भाव" in outcome.reply
    assert "बारिश" in outcome.reply
