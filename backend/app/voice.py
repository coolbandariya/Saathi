from dataclasses import dataclass

from .config import Settings
from .orchestrator import AgentContext, AgentOutcome, Orchestrator
from .provider_adapters import SafeProviderFactory


@dataclass(frozen=True)
class VoiceTurn:
    transcript: str
    outcome: AgentOutcome
    audio: bytes | None


class VoiceGateway:
    def __init__(self, settings: Settings, orchestrator: Orchestrator) -> None:
        self.orchestrator = orchestrator
        enabled = settings.speech_provider == "sarvam"
        self.stt = SafeProviderFactory.sarvam_stt(
            settings.sarvam_api_key if enabled else None,
            settings.sarvam_stt_endpoint,
            settings.sarvam_stt_model,
        )
        self.tts = SafeProviderFactory.sarvam_tts(
            settings.sarvam_api_key if enabled else None,
            settings.sarvam_tts_endpoint,
            settings.sarvam_tts_model,
            settings.sarvam_tts_speaker,
        )

    async def handle(self, audio: bytes, *, language: str, household_id: str | None) -> VoiceTurn:
        if self.stt is None:
            raise RuntimeError("speech_to_text_provider_not_configured")
        transcript = await self.stt.transcribe(audio, language=language)
        if not transcript:
            raise ValueError("empty_transcript")
        outcome = await self.orchestrator.handle(
            transcript,
            AgentContext(household_id=household_id, language=language),
        )
        audio_out = await self.tts.synthesize(outcome.reply, language=language) if self.tts else None
        return VoiceTurn(transcript=transcript, outcome=outcome, audio=audio_out)
