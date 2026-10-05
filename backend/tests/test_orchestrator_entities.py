import asyncio

from app.orchestrator import Orchestrator, AgentContext
from app.provenance import ToolResult


class FakeMandi:
    def __init__(self):
        self.calls = []

    async def price(self, **kwargs):
        self.calls.append(kwargs)
        return ToolResult(
            ok=True,
            data={
                "commodity": kwargs["commodity"],
                "market": kwargs.get("market") or "Karnal",
                "arrival_date": "2026-10-06",
                "modal_price": 2500,
            },
        )


def test_farming_message_changes_mandi_parameters():
    orchestrator = Orchestrator()
    fake = FakeMandi()
    orchestrator.mandi = fake
    outcome = asyncio.run(
        orchestrator.handle(
            "Karnal mandi me wheat ka rate batao",
            AgentContext(household_id=None),
        )
    )
    assert outcome.intent == "farming"
    assert fake.calls == [{
        "commodity": "Wheat",
        "state": "Haryana",
        "district": "Karnal",
        "market": "Karnal",
    }]
    assert "Karnal" in outcome.reply
