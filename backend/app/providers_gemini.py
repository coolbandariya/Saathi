from .providers import ChatRequest, ChatResponse

class GeminiProvider:
    def __init__(self, api_key: str, model: str) -> None:
        self.api_key = api_key
        self.model = model

    def chat(self, request: ChatRequest) -> ChatResponse:
        from google import genai
        client = genai.Client(api_key=self.api_key)
        response = client.models.generate_content(
            model=self.model,
            contents=request.message,
            config={
                "system_instruction": (
                    "You are Saathi. Never invent factual scheme, weather, mandi, "
                    "deadline, medical, or application-status data. Use tools for facts."
                )
            },
        )
        return ChatResponse(text=getattr(response, "text", None) or "Mujhe verified input chahiye.")
