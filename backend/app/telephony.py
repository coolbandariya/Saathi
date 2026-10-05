from typing import Protocol
import base64
import hashlib
import hmac

class TelephonyAdapter(Protocol):
    async def place_call(self, *, to: str, callback_url: str) -> str: ...

class HmacWebhookVerifier:
    def __init__(self, secret: str) -> None:
        self.secret = secret.encode()

    def verify(self, raw_body: bytes, signature: str) -> bool:
        expected = hmac.new(self.secret, raw_body, hashlib.sha256).digest()
        provided = signature.removeprefix("sha256=")
        try:
            return hmac.compare_digest(base64.b64encode(expected).decode(), provided) or hmac.compare_digest(expected.hex(), provided)
        except Exception:
            return False

class DemoTelephonyAdapter:
    async def place_call(self, *, to: str, callback_url: str) -> str:
        return "demo-call-accepted"
