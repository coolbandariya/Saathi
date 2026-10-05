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


class SarvamSpeechToTextProvider:
    def __init__(self, api_key: str, endpoint: str, model: str = "saaras:v4", mode: str = "transcribe", timeout_seconds: float = 20.0) -> None:
        self.api_key, self.endpoint, self.model, self.mode, self.timeout_seconds = api_key, endpoint, model, mode, timeout_seconds

    async def transcribe(self, audio: bytes, *, language: str) -> str:
        language_code = language if language == "unknown" or "-" in language else f"{language}-IN"
        async with httpx.AsyncClient(timeout=self.timeout_seconds) as client:
            response = await client.post(
                self.endpoint,
                headers={"api-subscription-key": self.api_key},
                files={"file": ("caller.webm", audio, "audio/webm")},
                data={"model": self.model, "mode": self.mode, "language_code": language_code},
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
            response = await client.post(
                self.endpoint,
                headers={"api-subscription-key": self.api_key, "Content-Type": "application/json"},
                json={"text": text[:2500], "model": self.model, "speaker": self.speaker, "language_code": language_code},
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
