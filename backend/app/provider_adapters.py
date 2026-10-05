import asyncio
import base64
import httpx

from .providers import ReasoningProvider, SpeechToTextProvider, TelephonyProvider, TextToSpeechProvider


class GeminiInteractionsProvider:
    def __init__(self, api_key: str, model: str = "gemini-3.8-flash", timeout_seconds: float = 15.0) -> None:
        self.api_key = api_key
        self.model = model
        self.timeout_seconds = timeout_seconds

    async def respond(self, messages: list[dict[str, str]]) -> str:
        prompt = "\n".join(f"{m.get('role', 'user')}: {m.get('content', '')}" for m in messages)
        body = {"model": self.model, "input": prompt}
        async with httpx.AsyncClient(timeout=self.timeout_seconds) as client:
            response = await client.post(
                "https://generativelanguage.googleapis.com/v1beta/interactions",
                headers={"x-goog-api-key": self.api_key, "Content-Type": "application/json"},
                json=body,
            )
            response.raise_for_status()
            data = response.json()
        return str(data.get("output_text") or "")


async def _request_with_retry(client, method: str, url: str, *, attempts: int = 3, **kwargs):
    for attempt in range(attempts):
        try:
            response = await client.request(method, url, **kwargs)
            if response.status_code not in {429, 500, 502, 503, 504} or attempt == attempts - 1:
                return response
        except httpx.RequestError:
            if attempt == attempts - 1:
                raise
        await asyncio.sleep(min(2 ** attempt, 4))
    raise RuntimeError("provider_request_failed")


class SarvamSpeechToTextProvider:
    def __init__(self, api_key: str, endpoint: str, model: str = "saaras:v4", mode: str = "transcribe", timeout_seconds: float = 20.0) -> None:
        self.api_key, self.endpoint, self.model, self.mode, self.timeout_seconds = api_key, endpoint, model, mode, timeout_seconds

    async def transcribe(self, audio: bytes, *, language: str) -> str:
        language_code = language if language == "unknown" or "-" in language else f"{language}-IN"
        async with httpx.AsyncClient(timeout=self.timeout_seconds) as client:
            response = await _request_with_retry(
                client, "POST", self.endpoint,
                headers={"api-subscription-key": self.api_key},
                files={"file": ("caller.webm", audio, "audio/webm")},
                data={"model": self.model, "mode": "codemix", "language_code": language_code},
            )
            response.raise_for_status()
            payload = response.json()
        return str(payload.get("transcript") or "").strip()


class SarvamTextToSpeechProvider:
    def __init__(self, api_key: str, endpoint: str, model: str = "bulbul:v3", speaker: str = "shubh", timeout_seconds: float = 20.0) -> None:
        self.api_key, self.endpoint, self.model, self.speaker, self.timeout_seconds = api_key, endpoint, model, speaker, timeout_seconds

    async def synthesize(self, text: str, *, language: str) -> bytes:
        language_code = language if language == "unknown" or "-" in language else f"{language}-IN"
        async with httpx.AsyncClient(timeout=self.timeout_seconds) as client:
            response = await _request_with_retry(
                client, "POST", self.endpoint,
                headers={"api-subscription-key": self.api_key, "Content-Type": "application/json"},
                json={"text": text[:2500], "model": self.model, "speaker": self.speaker, "language_code": language_code, "output_audio_codec": "wav"},
            )
            response.raise_for_status()
            body = response.json()
        audios = body.get("audios") or []
        if not audios:
            raise ValueError("sarvam_tts_returned_no_audio")
        return base64.b64decode(audios[0])


class ConfiguredSpeechToTextProvider:
    def __init__(self, endpoint: str, api_key: str, user_id: str | None = None, timeout_seconds: float = 15.0) -> None:
        self.endpoint, self.api_key, self.user_id, self.timeout_seconds = endpoint, api_key, user_id, timeout_seconds

    async def transcribe(self, audio: bytes, *, language: str) -> str:
        headers = {"Authorization": self.api_key}
        if self.user_id:
            headers["userId"] = self.user_id
        async with httpx.AsyncClient(timeout=self.timeout_seconds) as client:
            response = await client.post(self.endpoint, headers=headers, files={"audio": ("audio.wav", audio, "audio/wav")}, data={"language": language})
            response.raise_for_status()
            payload = response.json()
        return str(payload.get("text") or payload.get("transcript") or "")


class ConfiguredTextToSpeechProvider:
    def __init__(self, endpoint: str, api_key: str, user_id: str | None = None, timeout_seconds: float = 15.0) -> None:
        self.endpoint, self.api_key, self.user_id, self.timeout_seconds = endpoint, api_key, user_id, timeout_seconds

    async def synthesize(self, text: str, *, language: str) -> bytes:
        headers = {"Authorization": self.api_key, "Content-Type": "application/json"}
        if self.user_id:
            headers["userId"] = self.user_id
        async with httpx.AsyncClient(timeout=self.timeout_seconds) as client:
            response = await client.post(self.endpoint, headers=headers, json={"text": text, "language": language})
            response.raise_for_status()
        return response.content


class ExotelTelephonyProvider:
    def __init__(self, account_sid: str, api_key: str, api_token: str, caller_id: str, host: str = "api.in.exotel.com", timeout_seconds: float = 10.0) -> None:
        self.account_sid, self.api_key, self.api_token, self.caller_id, self.host, self.timeout_seconds = account_sid, api_key, api_token, caller_id, host, timeout_seconds

    async def place_call(self, *, to: str, callback_url: str) -> str:
        url = f"https://{self.host}/v1/Accounts/{self.account_sid}/Calls/connect"
        async with httpx.AsyncClient(timeout=self.timeout_seconds) as client:
            response = await client.post(
                url,
                data={"From": self.caller_id, "To": to, "CallerId": self.caller_id, "StatusCallback": callback_url},
                auth=(self.api_key, self.api_token),
            )
            response.raise_for_status()
            payload = response.json()
        return str(payload.get("Call", {}).get("Sid") or "")

    async def place_voice_ai_call(self, *, to: str, stream_url: str, callback_url: str | None = None) -> str:
        if not stream_url.startswith("wss://"):
            raise ValueError("Exotel Voice AI StreamUrl must use wss://")
        url = f"https://{self.host}/v1/Accounts/{self.account_sid}/Calls/connect"
        data = {
            "From": self.caller_id,
            "To": to,
            "CallerId": self.caller_id,
            "StreamUrl": stream_url,
            "StreamType": "bidirectional",
        }
        if callback_url:
            data["StatusCallback"] = callback_url
            data["StatusCallbackEvents[]"] = "terminal"
        async with httpx.AsyncClient(timeout=self.timeout_seconds) as client:
            response = await client.post(url, data=data, auth=(self.api_key, self.api_token))
            response.raise_for_status()
            payload = response.json()
        return str(payload.get("Call", {}).get("Sid") or "")


class SafeProviderFactory:
    @staticmethod
    def gemini(api_key: str | None, model: str) -> ReasoningProvider | None:
        return GeminiInteractionsProvider(api_key, model) if api_key else None

    @staticmethod
    def sarvam_stt(api_key: str | None, endpoint: str, model: str) -> SpeechToTextProvider | None:
        return SarvamSpeechToTextProvider(api_key, endpoint, model) if api_key else None

    @staticmethod
    def sarvam_tts(api_key: str | None, endpoint: str, model: str, speaker: str) -> TextToSpeechProvider | None:
        return SarvamTextToSpeechProvider(api_key, endpoint, model, speaker) if api_key else None


from dataclasses import dataclass
import json

@dataclass(frozen=True)
class GeminiToolCall:
    name: str
    arguments: dict
    call_id: str


class GeminiToolRouter:
    """Stateless Gemini Interactions function-calling boundary.

    The router only chooses a declared tool. Tool execution remains in Saathi,
    so factual authority stays with our adapters.
    """

    TOOLS = [
        {
            "type": "function",
            "name": "get_weather",
            "description": "Retrieve verified weather for caller context.",
            "parameters": {
                "type": "object",
                "properties": {"latitude": {"type": "number"}, "longitude": {"type": "number"}},
                "required": ["latitude", "longitude"],
            },
        },
        {
            "type": "function",
            "name": "get_mandi_price",
            "description": "Retrieve verified daily mandi price data.",
            "parameters": {
                "type": "object",
                "properties": {"commodity": {"type": "string"}, "state": {"type": "string"}, "district": {"type": "string"}},
                "required": ["commodity", "state"],
            },
        },
        {
            "type": "function",
            "name": "request_human",
            "description": "Escalate when the caller asks for a person or automation is unsafe/uncertain.",
            "parameters": {"type": "object", "properties": {"reason": {"type": "string"}}, "required": ["reason"]},
        },
    ]

    def __init__(self, api_key: str, model: str = "gemini-3.8-flash", timeout_seconds: float = 15.0) -> None:
        self.api_key, self.model, self.timeout_seconds = api_key, model, timeout_seconds

    async def choose(self, user_text: str) -> GeminiToolCall | None:
        async with httpx.AsyncClient(timeout=self.timeout_seconds) as client:
            response = await _request_with_retry(
                client, "POST",
                "https://generativelanguage.googleapis.com/v1beta/interactions",
                headers={"x-goog-api-key": self.api_key, "Content-Type": "application/json"},
                json={
                    "model": self.model,
                    "store": False,
                    "input": user_text,
                    "tools": self.TOOLS,
                },
            )
            response.raise_for_status()
            payload = response.json()

        for step in payload.get("steps", []):
            if step.get("type") != "function_call":
                continue
            arguments = step.get("arguments") or {}
            if isinstance(arguments, str):
                arguments = json.loads(arguments)
            return GeminiToolCall(
                name=str(step.get("name") or ""),
                arguments=arguments,
                call_id=str(step.get("id") or ""),
            )
        return None
