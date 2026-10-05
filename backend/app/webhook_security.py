import hashlib
import hmac
from dataclasses import dataclass, field


def verify_hmac_signature(
    *,
    payload: bytes,
    signature: str,
    secret: str,
    prefix: str = "sha256=",
) -> bool:
    if not signature or not secret:
        return False

    supplied = signature.removeprefix(prefix).strip()
    if len(supplied) != 64:
        return False

    expected = hmac.new(secret.encode("utf-8"), payload, hashlib.sha256).hexdigest()
    return hmac.compare_digest(supplied, expected)


@dataclass
class IdempotencyLedger:
    _seen: set[str] = field(default_factory=set)

    def accept(self, event_id: str) -> bool:
        normalized = event_id.strip()
        if not normalized or normalized in self._seen:
            return False
        self._seen.add(normalized)
        return True
