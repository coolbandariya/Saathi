import base64
import json
from dataclasses import dataclass

@dataclass(frozen=True)
class StreamStart:
    stream_sid: str
    call_sid: str
    sample_rate: int
    caller: str | None
    callee: str | None

def parse_start(event: dict) -> StreamStart:
    start = event.get("start") or {}
    media = start.get("media_format") or {}
    return StreamStart(
        stream_sid=str(start.get("stream_sid") or event.get("stream_sid") or ""),
        call_sid=str(start.get("call_sid") or ""),
        sample_rate=int(media.get("sample_rate") or 8000),
        caller=start.get("from"),
        callee=start.get("to"),
    )

def decode_media(event: dict) -> bytes:
    payload = ((event.get("media") or {}).get("payload") or "")
    return base64.b64decode(payload, validate=True) if payload else b""

def encode_media(stream_sid: str, pcm: bytes) -> str:
    return json.dumps({"event": "media", "stream_sid": stream_sid, "media": {"payload": base64.b64encode(pcm).decode("ascii")}})

def encode_mark(stream_sid: str, name: str) -> str:
    return json.dumps({"event": "mark", "stream_sid": stream_sid, "mark": {"name": name}})

def encode_clear(stream_sid: str) -> str:
    return json.dumps({"event": "clear", "stream_sid": stream_sid})
