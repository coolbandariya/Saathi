from .providers import ChatRequest, ChatResponse, SpeechRequest, SpeechResult

class DemoLLM:
    def chat(self, request: ChatRequest) -> ChatResponse:
        text = request.message.casefold()
        if any(x in text for x in ("weather", "मौसम")):
            return ChatResponse(text="मैं मौसम की जानकारी के लिए सत्यापित मौसम स्रोत देखूँगा।", tool_calls=[{"name": "weather.get_forecast", "arguments": {}}])
        if any(x in text for x in ("mandi", "मंडी")):
            return ChatResponse(text="मैं मंडी की कीमत के लिए सत्यापित कृषि स्रोत देखूँगा।", tool_calls=[{"name": "mandi.get_price", "arguments": {}}])
        if any(x in text for x in ("scholarship", "scheme", "yojana", "योजना", "छात्रवृत्ति")):
            return ChatResponse(text="मैं योजना की पात्रता और दस्तावेज़ सत्यापित करके बताऊँगा।", tool_calls=[{"name": "scheme.check", "arguments": {}}])
        return ChatResponse(text="मैं आपकी बात समझने और सही अगले कदम तक पहुँचाने में मदद करूँगा।")

class DemoSTT:
    def transcribe(self, request: SpeechRequest) -> SpeechResult:
        return SpeechResult(text="", language=request.language or "hi", confidence=0.0)

class DemoTTS:
    def synthesize(self, text: str, language: str = "hi") -> bytes:
        return text.encode("utf-8")
