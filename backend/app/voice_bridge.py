import json
import math
from typing import Any, Awaitable, Callable

from .exotel_stream import decode_media, encode_media, parse_start


def _is_silent(pcm: bytes, *, threshold: int = 450) -> bool:
    """Cheap PCM16 RMS gate for the bounded-turn adapter.

    This is only a turn-boundary heuristic. Sarvam realtime VAD is the
    production replacement and should be preferred once deployed.
    """
    if len(pcm) < 320:
        return False
    samples = memoryview(pcm[: len(pcm) - (len(pcm) % 2)]).cast("h")
    if not samples:
        return False
    rms = math.sqrt(sum(sample * sample for sample in samples) / len(samples))
    return rms < threshold


async def run_exotel_session(
    websocket: Any,
    *,
    transcribe: Callable[[bytes, int], Awaitable[str]],
    respond: Callable[[str], Awaitable[str]],
    synthesize: Callable[[str, int], Awaitable[bytes]],
    max_turn_seconds: float = 8.0,
    silence_seconds: float = 0.6,
    min_turn_seconds: float = 0.25,
) -> None:
    """Run one bounded-turn bidirectional Exotel media session.

    The adapter uses PCM silence as a conservative turn boundary and flushes
    the final partial turn on stop. It is still not a realtime streaming
    implementation; Sarvam realtime STT + server VAD is the production path.
    """
    if max_turn_seconds <= 0 or silence_seconds <= 0 or min_turn_seconds <= 0:
        raise ValueError("turn timing values must be positive")
    if min_turn_seconds >= max_turn_seconds:
        raise ValueError("min_turn_seconds must be below max_turn_seconds")

    stream_sid: str | None = None
    sample_rate = 8000
    audio_buffer = bytearray()
    silent_bytes = 0
    saw_speech = False

    async def process_turn() -> None:
        nonlocal audio_buffer, silent_bytes, saw_speech
        if not audio_buffer:
            return
        pcm = bytes(audio_buffer)
        audio_buffer.clear()
        silent_bytes = 0
        saw_speech = False
        transcript = await transcribe(pcm, sample_rate)
        if not transcript.strip():
            return
        reply = await respond(transcript)
        if not reply.strip():
            return
        audio = await synthesize(reply, sample_rate)
        if stream_sid and audio:
            await websocket.send(encode_media(stream_sid, audio))

    async for raw in websocket:
        try:
            event = json.loads(raw)
        except (TypeError, json.JSONDecodeError):
            continue

        event_type = event.get("event")
        if event_type == "connected":
            continue

        if event_type == "start":
            start = parse_start(event)
            if not start.stream_sid or not start.call_sid:
                raise ValueError("invalid_exotel_start_event")
            if start.sample_rate not in {8000, 16000, 24000}:
                raise ValueError("unsupported_exotel_sample_rate")
            stream_sid, sample_rate = start.stream_sid, start.sample_rate
            audio_buffer.clear()
            silent_bytes = 0
            saw_speech = False
            continue

        if event_type == "media":
            try:
                pcm = decode_media(event)
            except (ValueError, TypeError):
                continue
            if not pcm:
                continue

            audio_buffer.extend(pcm)
            frame_bytes = max(2, int(sample_rate * 2 * 0.1))
            frame = pcm[-frame_bytes:]
            frame_silent = _is_silent(frame)
            if frame_silent:
                silent_bytes += len(frame)
            else:
                silent_bytes = 0
                saw_speech = True

            duration = len(audio_buffer) / (sample_rate * 2)
            silence_duration = silent_bytes / (sample_rate * 2)
            if saw_speech and duration >= min_turn_seconds and silence_duration >= silence_seconds:
                await process_turn()
            elif duration >= max_turn_seconds:
                await process_turn()
            continue

        if event_type == "stop":
            await process_turn()
            break

        # DTMF/mark events are deliberately ignored by the bounded MVP bridge.
        # They remain part of the protocol surface for a future barge-in/handoff path.
