import asyncio

from app.orchestrator import AgentContext, Orchestrator
from app.schemas import LocationContext


def test_golden_demo_harness_is_deterministic_and_truthful(monkeypatch) -> None:
    from app import orchestrator as module
    class FakeSettings:
        demo_mode = True
        gemini_api_key = None
        llm_model = "demo"
        mandi_api_key = None
        mandi_resource_id = None
        mandi_api_base = ""
    monkeypatch.setattr(module, "get_settings", lambda: FakeSettings())
    orchestrator = Orchestrator()
    context = AgentContext(
        household_id="demo-household",
        language="hi",
        location=LocationContext(latitude=28.9931, longitude=77.0151, label="Sonipat demo context"),
    )

    mandi = asyncio.run(orchestrator.handle("हरियाणा सोनीपत मंडी में गेहूं का भाव", context))
    weather = asyncio.run(orchestrator.handle("अगले 24 घंटे में बारिश की संभावना कितनी है?", context))
    scheme = asyncio.run(orchestrator.handle("मुझे किसान की सरकारी योजना बताओ", context))
    human = asyncio.run(orchestrator.handle("मुझे किसी इंसान से बात करनी है", context))

    assert mandi.intent == "farming"
    assert mandi.result is not None and mandi.result.source is not None
    assert weather.intent == "farming"
    assert weather.result is not None and weather.result.source is not None
    assert scheme.intent == "scheme"
    assert scheme.result is not None and scheme.result.source is not None
    assert human.intent == "human"
    assert human.escalated is True
    assert human.escalation_reason == "explicit_human_request"

    # The demo must never turn a synthetic provider result into an unlabeled live claim.
    for outcome in (mandi, weather, scheme):
        assert outcome.result.source.freshness_note
