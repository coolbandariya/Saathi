import logging
import uuid
from fastapi import Request

logger=logging.getLogger("saathi")

def request_id(request: Request) -> str:
    return request.headers.get("x-request-id") or str(uuid.uuid4())

def log_request(method: str, path: str, request_id_value: str, status_code: int, latency_ms: float) -> None:
    logger.info("request method=%s path=%s request_id=%s status=%s latency_ms=%.1f", method, path, request_id_value, status_code, latency_ms)
