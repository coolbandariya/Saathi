from datetime import datetime, timezone
from .consent import ConsentState, can_make_outbound_call
from .domain import Task

def due_tasks(tasks: list[Task], now: datetime | None = None) -> list[Task]:
    now=now or datetime.now(timezone.utc)
    return [t for t in tasks if t.status=="open" and t.due_at is not None and t.due_at<=now]

def callback_candidates(tasks: list[Task], consent: ConsentState, now: datetime | None = None) -> list[Task]:
    now=now or datetime.now(timezone.utc)
    if not can_make_outbound_call(consent, now): return []
    return [t for t in due_tasks(tasks, now) if t.outbound_consent]
