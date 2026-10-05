from typing import Protocol


class SpeechToTextProvider(Protocol):
    async def transcribe(self, audio: bytes, *, language: str) -> str: ...


class TextToSpeechProvider(Protocol):
    async def synthesize(self, text: str, *, language: str) -> bytes: ...


class ReasoningProvider(Protocol):
    async def respond(self, messages: list[dict[str, str]]) -> str: ...


class TelephonyProvider(Protocol):
    async def place_call(self, *, to: str, callback_url: str) -> str: ...
