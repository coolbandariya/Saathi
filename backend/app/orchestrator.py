from __future__ import annotations

from dataclasses import dataclass

from .config import get_settings
from .escalation import EscalationPolicy, EscalationReason
from .http_tools import DataGovMandiTool, OpenMeteoWeatherTool
from .intent import classify_intent, extract_farming_entities
from .provenance import ToolResult
from .schemas import Intent, LocationContext
from .tools import DemoMandiTool, DemoWeatherTool, PMKisanSchemeTool


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
    tool_name: str | None = None


class Orchestrator:
    def __init__(self) -> None:
        settings = get_settings()
        if settings.demo_mode:
            self.weather = DemoWeatherTool()
            self.mandi = DemoMandiTool()
        else:
            self.weather = OpenMeteoWeatherTool()
            self.mandi = (
                DataGovMandiTool(
                    api_key=settings.mandi_api_key,
                    resource_id=settings.mandi_resource_id,
                    api_base=settings.mandi_api_base,
                )
                if settings.mandi_api_key and settings.mandi_resource_id
                else None
            )
        self.escalation = EscalationPolicy()
        self.scheme = PMKisanSchemeTool()

    def _outcome(
        self,
        *,
        intent: Intent,
        reply: str,
        result: ToolResult | None = None,
        confidence: float = 0.9,
        explicit_human_request: bool = False,
        safety_boundary: bool = False,
        tool_name: str | None = None,
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
            tool_name=tool_name,
        )

    async def handle(self, message: str, context: AgentContext) -> AgentOutcome:
        intent = classify_intent(message)

        if intent == "human":
            return self._outcome(
                intent=intent,
                reply="ठीक है। मैं आपकी बात volunteer सहायता के लिए भेजने की तैयारी कर रहा हूँ।",
                confidence=1.0,
                explicit_human_request=True,
                tool_name="request_human",
            )

        if intent == "farming":
            lowered = message.casefold()
            if any(x in lowered for x in ("मौसम", "बारिश", "weather", "rain")):
                location = context.location
                if location is None:
                    return self._outcome(
                        intent=intent,
                        reply="मौसम बताने के लिए आपका शहर या स्थान चाहिए। कृपया अपना जिला या स्थान बताइए।",
                        confidence=0.72,
                        tool_name="get_weather",
                    )
                result = await self.weather.forecast(latitude=location.latitude, longitude=location.longitude)
                if result.ok:
                    d = result.data
                    probability = d.get("rain_probability_pct", d.get("next_24h_rain_probability_max", 0))
                    return self._outcome(
                        intent=intent,
                        reply=f"उपलब्ध मौसम जानकारी के अनुसार तापमान {d['temperature_c']}°C है और अगले 24 घंटे में बारिश की अधिकतम संभावना {probability}% है।",
                        result=result,
                        tool_name="get_weather",
                    )
                return self._outcome(
                    intent=intent,
                    reply="अभी मौसम की जानकारी उपलब्ध नहीं है। मैं गलत जानकारी नहीं देना चाहता।",
                    result=result,
                    confidence=0.55,
                    tool_name="get_weather",
                )

            if self.mandi is None:
                return self._outcome(
                    intent=intent,
                    reply="मंडी का लाइव सरकारी स्रोत अभी configured नहीं है। मैं डेमो भाव को live भाव बताकर नहीं दिखाऊँगा।",
                    confidence=0.55,
                    tool_name="get_mandi_price",
                )

            entities = extract_farming_entities(message)
            missing = []
            if not entities.commodity:
                missing.append("फसल")
            if not entities.state:
                missing.append("राज्य")
            if not entities.district and not entities.market:
                missing.append("जिला या मंडी")

            if missing:
                return self._outcome(
                    intent=intent,
                    reply="मंडी का सही सरकारी भाव बताने के लिए " + " और ".join(missing) + " बताइए।",
                    confidence=0.78,
                    tool_name="get_mandi_price",
                )

            result = await self.mandi.price(
                commodity=entities.commodity,
                state=entities.state,
                district=entities.district,
                market=entities.market,
            )
            if result.ok:
                d = result.data
                market = d.get("market") or entities.market or entities.district or entities.state
                date = d.get("arrival_date") or "latest returned date"
                return self._outcome(
                    intent=intent,
                    reply=f"सरकारी बाजार डेटा के अनुसार {market} में {d['commodity']} का मॉडल भाव ₹{d['modal_price']} प्रति क्विंटल है (डेटा दिनांक {date})।",
                    result=result,
                    tool_name="get_mandi_price",
                )
            return self._outcome(
                intent=intent,
                reply="अभी सरकारी मंडी स्रोत से विश्वसनीय भाव नहीं मिला। मैं अनुमान नहीं दूँगा।",
                result=result,
                confidence=0.55,
                tool_name="get_mandi_price",
            )

        if intent == "scheme" and any(x in message.casefold() for x in ("किसान", "pm-kisan", "pm kisan", "किसान योजना")):
            result = await self.scheme.explain()
            return self._outcome(
                intent=intent,
                reply="आधिकारिक PM-KISAN जानकारी के अनुसार पात्र landholding farmer families के लिए सालाना ₹6,000 तीन बराबर किस्तों में दिए जाते हैं और registered farmers के लिए eKYC mandatory है। अंतिम eligibility सरकार की scheme guidelines और verification पर निर्भर है।",
                result=result,
                confidence=0.96,
                tool_name="get_pmkisan_info",
            )

        replies = {
            "scheme": "मैं सरकारी योजनाओं की पात्रता और जरूरी दस्तावेज़ समझाने में मदद कर सकता हूँ।",
            "document": "मैं दस्तावेज़ का पाठ समझाने और जरूरी अगला कदम निकालने में मदद कर सकता हूँ।",
            "task": "मैं इसे आपके लिए follow-up task के रूप में रखने में मदद कर सकता हूँ।",
            "general": "नमस्ते! मैं साथी हूँ। आप अपनी जरूरत हिंदी में बताइए।",
        }
        return self._outcome(intent=intent, reply=replies[intent])
