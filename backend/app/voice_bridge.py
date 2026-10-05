import json
import math
from typing import Any, Awaitable, Callable

from .exotel_stream import decode_media, encode_clear, encode_media, parse_start


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
    playback_active = False

    async def process_turn() -> None:
        nonlocal audio_buffer, silent_bytes, saw_speech, playback_active
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
            playback_active = True
            await websocket.send(encode_media(stream_sid, audio))
            # Exotel can interrupt buffered output when the caller starts speaking again.
            # The next inbound speech frame clears the remote playback buffer.


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
            playback_active = False
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
                if playback_active and stream_sid:
                    await websocket.send(encode_clear(stream_sid))
                    playback_active = False
                saw_speech = True

            duration = len(audio_buffer) / (sample_rate * 2)
            silence_duration = silent_bytes / (sample_rate * 2)
            if saw_speech and duration >= min_turn_seconds and silence_duration >= silence_seconds:
                await process_turn()
            elif duration >= max_turn_seconds:
                await process_turn()
            continue

        if event_type == "stop":
            playback_active = False
            await process_turn()
            break

        # DTMF/mark events are deliberately ignored by the bounded MVP bridge.
        # They remain part of the protocol surface for a future barge-in/handoff path.


async def run_exotel_realtime_session(
    websocket: Any,
    *,
    stt_session: Any,
    respond: Callable[[str], Awaitable[str]],
    synthesize_stream: Callable[[str, int], Any],
) -> None:
    """Run a genuine streaming STT + streaming TTS Exotel session.

    Exotel PCM is forwarded continuously to Sarvam Realtime STT. Final
    transcripts become turns without buffering a whole utterance locally.
    Sarvam VAD drives turn boundaries and speech-start events cancel/clear
    agent playback for deterministic barge-in.
    """
    import asyncio

    stream_sid: str | None = None
    sample_rate = 8000
    playback_task: asyncio.Task | None = None
    response_tasks: set[asyncio.Task] = set()
    reader_task: asyncio.Task | None = None

    async def cancel_playback() -> None:
        nonlocal playback_task
        if playback_task and not playback_task.done():
            playback_task.cancel()
            try:
                await playback_task
            except asyncio.CancelledError:
                pass
        playback_task = None
        if stream_sid:
            await websocket.send(encode_clear(stream_sid))

    async def speak(reply: str) -> None:
        if not stream_sid:
            return
        async for chunk in synthesize_stream(reply, sample_rate):
            if not chunk:
                continue
            await websocket.send(encode_media(stream_sid, chunk))

    async def process_transcript(transcript: str) -> None:
        nonlocal playback_task
        if not transcript.strip():
            return
        await cancel_playback()
        reply = await respond(transcript)
        if not reply.strip():
            return
        playback_task = asyncio.create_task(speak(reply))

    async def stt_reader() -> None:
        nonlocal playback_task
        while True:
            event = await stt_session.receive()
            event_name = event.get("event")
            if event_name == "vad.speech_start":
                await cancel_playback()
            elif event_name == "transcript.final":
                text = str(event.get("text") or "").strip()
                if text:
                    task = asyncio.create_task(process_transcript(text))
                    response_tasks.add(task)
                    task.add_done_callback(response_tasks.discard)
            elif event_name == "error":
                if event.get("is_fatal"):
                    raise RuntimeError("sarvam_realtime_stt_fatal")

    try:
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
                if start.sample_rate not in {8000, 16000}:
                    raise ValueError("realtime_bridge_requires_8k_or_16k")
                stream_sid, sample_rate = start.stream_sid, start.sample_rate
                await stt_session.connect(sample_rate=sample_rate)
                reader_task = asyncio.create_task(stt_reader())
                continue

            if event_type == "media":
                try:
                    pcm = decode_media(event)
                except (ValueError, TypeError):
                    continue
                if pcm:
                    await stt_session.send_audio(pcm)
                continue

            if event_type == "stop":
                break

        if stream_sid:
            await stt_session.close()
    finally:
        if reader_task and not reader_task.done():
            reader_task.cancel()
            await asyncio.gather(reader_task, return_exceptions=True)
        await cancel_playback()
        for task in list(response_tasks):
            task.cancel()
        if response_tasks:
            await asyncio.gather(*response_tasks, return_exceptions=True)
        try:
            await stt_session.close()
        except Exception:
            pass
