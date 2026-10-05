from __future__ import annotations

from dataclasses import dataclass

from .escalation import EscalationPolicy, EscalationReason
from .intent import classify_intent
from .provenance import ToolResult
from .schemas import Intent, LocationContext
from .tools import DemoMandiTool, DemoWeatherTool


@dataclass(frozen=True)
class AgentContext:
    household_id: str | None
    language: str = "hi"
    location: LocationContext | None = None


@dataclass(frozen=True)
class AgentOutcome:
    intent: Intent
    reply: str
    result: ToolResult | None
    confidence: float
    escalated: bool
    escalation_reason: EscalationReason | None


class Orchestrator:
    def __init__(self) -> None:
        self.weather = DemoWeatherTool()
        self.mandi = DemoMandiTool()
        self.escalation = EscalationPolicy()

    def _outcome(
        self,
        *,
        intent: Intent,
        reply: str,
        result: ToolResult | None = None,
        confidence: float = 0.9,
        explicit_human_request: bool = False,
        safety_boundary: bool = False,
    ) -> AgentOutcome:
        decision = self.escalation.evaluate(
            confidence=confidence,
            explicit_human_request=explicit_human_request,
            provider_failed=bool(result and not result.ok),
            safety_boundary=safety_boundary,
        )
        return AgentOutcome(
            intent=intent,
            reply=reply,
            result=result,
            confidence=decision.confidence,
            escalated=decision.escalate,
            escalation_reason=decision.reason,
        )

    async def handle(self, message: str, context: AgentContext) -> AgentOutcome:
        intent = classify_intent(message)

        if intent == "human":
            return self._outcome(
                intent=intent,
                reply="ठीक है। मैं आपकी बात volunteer सहायता के लिए भेजने की तैयारी कर रहा हूँ।",
                confidence=1.0,
                explicit_human_request=True,
            )

        if intent == "farming":
            lowered = message.casefold()
            if any(x in lowered for x in ("मौसम", "बारिश", "weather", "rain")):
                location = context.location
                latitude = location.latitude if location else 28.99
                longitude = location.longitude if location else 77.02
                result = await self.weather.forecast(latitude=latitude, longitude=longitude)
                if result.ok:
                    d = result.data
                    return self._outcome(
                        intent=intent,
                        reply=f"अभी उपलब्ध जानकारी के अनुसार तापमान {d['temperature_c']}°C है और बारिश की संभावना {d['rain_probability_pct']}% है।",
                        result=result,
                    )
                return self._outcome(
                    intent=intent,
                    reply="अभी मौसम की जानकारी उपलब्ध नहीं है। मैं गलत जानकारी नहीं देना चाहता।",
                    result=result,
                    confidence=0.55,
                )

            result = await self.mandi.price(commodity="गेहूं", state="Haryana", district="Sonipat")
            if result.ok:
                d = result.data
                return self._outcome(
                    intent=intent,
                    reply=f"डेमो मंडी डेटा के अनुसार {d['commodity']} का मॉडल भाव ₹{d['modal_price']} प्रति क्विंटल है। यह डेमो डेटा है, लाइव भाव नहीं।",
                    result=result,
                )
            return self._outcome(intent=intent, reply="अभी मंडी की जानकारी उपलब्ध नहीं है।", result=result, confidence=0.55)

        replies = {
            "scheme": "मैं सरकारी योजनाओं की पात्रता और जरूरी दस्तावेज़ समझाने में मदद कर सकता हूँ।",
            "document": "मैं दस्तावेज़ का पाठ समझाने और जरूरी अगला कदम निकालने में मदद कर सकता हूँ।",
            "task": "मैं इसे आपके लिए follow-up task के रूप में रखने में मदद कर सकता हूँ।",
            "general": "नमस्ते! मैं साथी हूँ। आप अपनी जरूरत हिंदी में बताइए।",
        }
        return self._outcome(intent=intent, reply=replies[intent])
