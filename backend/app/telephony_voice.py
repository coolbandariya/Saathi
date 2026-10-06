from __future__ import annotations

import base64
import io
import wave
from typing import Any

import httpx

from .config import Settings


class SarvamTelephonySpeechProvider:
    """Short-turn Sarvam speech adapter for Exotel PCM.

    This is intentionally a bounded turn adapter, not a claim of low-latency
    realtime streaming. A realtime transport can replace these methods later.
    """

    def __init__(self, settings: Settings, timeout_seconds: float = 20.0) -> None:
        if not settings.sarvam_api_key:
            raise RuntimeError("speech_provider_not_configured")
        self.api_key = settings.sarvam_api_key
        self.stt_endpoint = settings.sarvam_stt_endpoint
        self.stt_model = settings.sarvam_stt_model
        self.tts_endpoint = settings.sarvam_tts_endpoint
        self.tts_model = settings.sarvam_tts_model
        self.tts_speaker = settings.sarvam_tts_speaker
        self.timeout_seconds = timeout_seconds

    @staticmethod
    def pcm_to_wav(pcm: bytes, sample_rate: int) -> bytes:
        if sample_rate not in {8000, 16000, 24000}:
            raise ValueError("unsupported_telephony_sample_rate")
        buffer = io.BytesIO()
        with wave.open(buffer, "wb") as wav:
            wav.setnchannels(1)
            wav.setsampwidth(2)
            wav.setframerate(sample_rate)
            wav.writeframes(pcm)
        return buffer.getvalue()

    async def transcribe(self, pcm: bytes, *, sample_rate: int, language: str = "hi-IN") -> str:
        wav = self.pcm_to_wav(pcm, sample_rate)
        language_code = language if "-" in language else f"{language}-IN"
        async with httpx.AsyncClient(timeout=self.timeout_seconds) as client:
            response = await client.post(
                self.stt_endpoint,
                headers={"api-subscription-key": self.api_key},
                files={"file": ("caller.wav", wav, "audio/wav")},
                data={"model": self.stt_model, "mode": "codemix", "language_code": language_code},
            )
            response.raise_for_status()
            body: dict[str, Any] = response.json()
        return str(body.get("transcript") or "").strip()

    async def synthesize(self, text: str, *, sample_rate: int, language: str = "hi-IN") -> bytes:
        if sample_rate not in {8000, 16000, 24000}:
            raise ValueError("unsupported_telephony_sample_rate")
        language_code = language if "-" in language else f"{language}-IN"
        async with httpx.AsyncClient(timeout=self.timeout_seconds) as client:
            response = await client.post(
                self.tts_endpoint,
                headers={"api-subscription-key": self.api_key, "Content-Type": "application/json"},
                json={
                    "text": text[:2500],
                    "model": self.tts_model,
                    "speaker": self.tts_speaker,
                    "language_code": language_code,
                    "speech_sample_rate": sample_rate,
                    "output_audio_codec": "linear16",
                },
            )
            response.raise_for_status()
            body: dict[str, Any] = response.json()
        audios = body.get("audios") or []
        if not audios:
            raise ValueError("sarvam_tts_returned_no_audio")
        return base64.b64decode("".join(audios))
