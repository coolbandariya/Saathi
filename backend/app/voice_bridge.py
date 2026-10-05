import json
from typing import Any, Awaitable, Callable

from .exotel_stream import decode_media, encode_media, parse_start


async def run_exotel_session(
    websocket: Any,
    *,
    transcribe: Callable[[bytes, int], Awaitable[str]],
    respond: Callable[[str], Awaitable[str]],
    synthesize: Callable[[str, int], Awaitable[bytes]],
    max_turn_seconds: float = 2.0,
) -> None:
    """Run one bounded-turn bidirectional Exotel media session.

    Provider calls are injected so tests stay deterministic. The bridge does not
    claim realtime behavior: it batches audio into short turns and flushes the
    final partial turn on stop.
    """
    if max_turn_seconds <= 0:
        raise ValueError("max_turn_seconds must be positive")

    stream_sid: str | None = None
    sample_rate = 8000
    audio_buffer = bytearray()

    async def process_turn() -> None:
        nonlocal audio_buffer
        if not audio_buffer:
            return
        pcm = bytes(audio_buffer)
        audio_buffer.clear()
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
            continue

        if event_type == "media":
            try:
                audio_buffer.extend(decode_media(event))
            except (ValueError, TypeError):
                continue
            max_bytes = int(sample_rate * 2 * max_turn_seconds)
            if len(audio_buffer) >= max_bytes:
                await process_turn()
            continue

        if event_type == "stop":
            await process_turn()
            break

        # DTMF/mark events are deliberately ignored by the bounded MVP bridge.
        # They remain part of the protocol surface for a future barge-in/handoff path.
