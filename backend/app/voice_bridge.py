import json
from typing import Any, Awaitable, Callable

from .exotel_stream import decode_media, encode_media, parse_start

async def run_exotel_session(
    websocket: Any,
    *,
    transcribe: Callable[[bytes, int], Awaitable[str]],
    respond: Callable[[str], Awaitable[str]],
    synthesize: Callable[[str, int], Awaitable[bytes]],
) -> None:
    """Run one bidirectional Exotel media session.

    The adapter deliberately keeps provider calls injected so tests can use deterministic
    fakes and production can supply Sarvam realtime STT/TTS later.
    """
    stream_sid = None
    sample_rate = 8000
    audio_buffer = bytearray()

    async for raw in websocket:
        event = json.loads(raw)
        event_type = event.get("event")

        if event_type == "start":
            start = parse_start(event)
            stream_sid, sample_rate = start.stream_sid, start.sample_rate
            continue

        if event_type == "media":
            audio_buffer.extend(decode_media(event))
            # Keep this bounded. A realtime STT implementation should replace this
            # accumulation with incremental websocket audio forwarding.
            if len(audio_buffer) >= sample_rate * 2:
                transcript = await transcribe(bytes(audio_buffer), sample_rate)
                audio_buffer.clear()
                if not transcript.strip():
                    continue
                reply = await respond(transcript)
                if not reply.strip():
                    continue
                audio = await synthesize(reply, sample_rate)
                if stream_sid and audio:
                    await websocket.send(encode_media(stream_sid, audio))
            continue

        if event_type == "stop":
            break
