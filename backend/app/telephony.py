import base64, hashlib, hmac, json
from typing import Literal
from pydantic import BaseModel

class CallEvent(BaseModel):
    event: Literal["connected", "start", "media", "dtmf", "mark", "stop", "clear"]
    stream_sid: str | None = None
    call_sid: str | None = None
    payload: str | None = None
    metadata: dict = {}

class WebhookReplayGuard:
    def __init__(self) -> None: self._seen: set[str] = set()
    def accept(self, event_id: str) -> bool:
        if not event_id or event_id in self._seen: return False
        self._seen.add(event_id); return True

def verify_hmac_signature(raw_body: bytes, signature: str, secret: str) -> bool:
    if not secret or not signature: return False
    expected = hmac.new(secret.encode(), raw_body, hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected, signature)

def parse_exotel_event(raw: str) -> CallEvent:
    data=json.loads(raw); event=data.get("event")
    if event not in {"connected","start","media","dtmf","mark","stop","clear"}: raise ValueError("unsupported Exotel stream event")
    start=data.get("start") or {}; stop=data.get("stop") or {}; media=data.get("media") or {}
    return CallEvent(event=event, stream_sid=data.get("stream_sid") or start.get("stream_sid") or stop.get("stream_sid"), call_sid=start.get("call_sid") or stop.get("call_sid"), payload=media.get("payload"), metadata=data)

def encode_media(stream_sid: str, pcm: bytes) -> str:
    return json.dumps({"event":"media","stream_sid":stream_sid,"media":{"payload":base64.b64encode(pcm).decode("ascii")}})
