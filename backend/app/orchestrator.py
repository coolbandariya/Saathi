from dataclasses import dataclass
from .intent import classify_intent
from .schemas import Intent
from .tools import DemoWeatherTool, DemoMandiTool
from .provenance import ToolResult
from .escalation import EscalationPolicy

@dataclass
class AgentContext:
    household_id: str | None
    language: str = "hi"

class Orchestrator:
    def __init__(self) -> None:
        self.weather = DemoWeatherTool()
        self.mandi = DemoMandiTool()
        self.escalation = EscalationPolicy()

    async def handle(self, message: str, context: AgentContext) -> tuple[Intent, str, ToolResult | None]:
        intent = classify_intent(message)

        if intent == "human":
            return intent, "ठीक है। मैं आपकी बात volunteer सहायता के लिए भेजने की तैयारी कर रहा हूँ।", None

        if intent == "farming":
            lowered = message.casefold()
            if any(x in lowered for x in ("मौसम", "बारिश", "weather", "rain")):
                result = await self.weather.forecast(latitude=28.99, longitude=77.02)
                if result.ok:
                    d = result.data
                    return intent, f"अभी उपलब्ध जानकारी के अनुसार तापमान {d['temperature_c']}°C है और बारिश की संभावना {d['rain_probability_pct']}% है।", result
                return intent, "अभी मौसम की जानकारी उपलब्ध नहीं है। मैं गलत जानकारी नहीं देना चाहता।", result

            result = await self.mandi.price(commodity="गेहूं", state="Haryana", district="Sonipat")
            if result.ok:
                d = result.data
                return intent, f"डेमो मंडी डेटा के अनुसार {d['commodity']} का मॉडल भाव ₹{d['modal_price']} प्रति क्विंटल है। यह डेमो डेटा है, लाइव भाव नहीं।", result
            return intent, "अभी मंडी की जानकारी उपलब्ध नहीं है।", result

        replies = {
            "scheme": "मैं सरकारी योजनाओं की पात्रता और जरूरी दस्तावेज़ समझाने में मदद कर सकता हूँ।",
            "document": "मैं दस्तावेज़ का पाठ समझाने और जरूरी अगला कदम निकालने में मदद कर सकता हूँ।",
            "task": "मैं इसे आपके लिए follow-up task के रूप में रखने में मदद कर सकता हूँ।",
            "general": "नमस्ते! मैं साथी हूँ। आप अपनी जरूरत हिंदी में बताइए।",
        }
        return intent, replies[intent], None
