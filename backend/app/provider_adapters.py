import base64
import httpx
from typing import Any
from .providers import ReasoningProvider, SpeechToTextProvider, TextToSpeechProvider, TelephonyProvider

class GeminiInteractionsProvider:
    def __init__(self, api_key: str, model: str = "gemini-3.8-flash", timeout_seconds: float = 15.0) -> None:
        self.api_key=api_key
        self.model=model
        self.timeout_seconds=timeout_seconds

    async def respond(self, messages: list[dict[str,str]]) -> str:
        prompt="\n".join(f"{m.get('role','user')}: {m.get('content','')}" for m in messages)
        body={"model":self.model,"input":prompt}
        async with httpx.AsyncClient(timeout=self.timeout_seconds) as client:
            response=await client.post("https://generativelanguage.googleapis.com/v1beta/interactions",headers={"x-goog-api-key":self.api_key,"Content-Type":"application/json"},json=body)
            response.raise_for_status()
            data=response.json()
        return data.get("output_text","") or ""

class ConfiguredSpeechToTextProvider:
    def __init__(self, endpoint: str, api_key: str, user_id: str | None = None, timeout_seconds: float = 15.0) -> None:
        self.endpoint=endpoint
        self.api_key=api_key
        self.user_id=user_id
        self.timeout_seconds=timeout_seconds

    async def transcribe(self, audio: bytes, *, language: str) -> str:
        headers={"Authorization":self.api_key}
        if self.user_id:
            headers["userId"]=self.user_id
        files={"audio":("audio.wav",audio,"audio/wav")}
        data={"language":language}
        async with httpx.AsyncClient(timeout=self.timeout_seconds) as client:
            response=await client.post(self.endpoint,headers=headers,files=files,data=data)
            response.raise_for_status()
            payload=response.json()
        return str(payload.get("text") or payload.get("transcript") or "")

class ConfiguredTextToSpeechProvider:
    def __init__(self, endpoint: str, api_key: str, user_id: str | None = None, timeout_seconds: float = 15.0) -> None:
        self.endpoint=endpoint
        self.api_key=api_key
        self.user_id=user_id
        self.timeout_seconds=timeout_seconds

    async def synthesize(self, text: str, *, language: str) -> bytes:
        headers={"Authorization":self.api_key,"Content-Type":"application/json"}
        if self.user_id:
            headers["userId"]=self.user_id
        async with httpx.AsyncClient(timeout=self.timeout_seconds) as client:
            response=await client.post(self.endpoint,headers=headers,json={"text":text,"language":language})
            response.raise_for_status()
        return response.content

class ExotelTelephonyProvider:
    def __init__(self, account_sid: str, api_key: str, api_token: str, caller_id: str, host: str = "api.in.exotel.com", timeout_seconds: float = 10.0) -> None:
        self.account_sid=account_sid
        self.api_key=api_key
        self.api_token=api_token
        self.caller_id=caller_id
        self.host=host
        self.timeout_seconds=timeout_seconds

    async def place_call(self, *, to: str, callback_url: str) -> str:
        url=f"https://{self.host}/v1/Accounts/{self.account_sid}/Calls/connect"
        data={"From":self.caller_id,"To":to,"CallerId":self.caller_id,"StatusCallback":callback_url}
        async with httpx.AsyncClient(timeout=self.timeout_seconds) as client:
            response=await client.post(url,data=data,auth=(self.api_key,self.api_token))
            response.raise_for_status()
            payload=response.json()
        call=payload.get("Call",{})
        return str(call.get("Sid") or "")

class SafeProviderFactory:
    """Creates real providers only when their required configuration is present."""
    @staticmethod
    def gemini(api_key: str | None, model: str) -> ReasoningProvider | None:
        return GeminiInteractionsProvider(api_key,model) if api_key else None
