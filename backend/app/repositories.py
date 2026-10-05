from datetime import datetime
from typing import Protocol

from .domain import Consent, ConsentType, Task, TaskStatus


class ConsentRepository(Protocol):
    async def get(self, *, household_id: str, consent_type: ConsentType) -> Consent | None: ...

    async def save(self, consent: Consent) -> Consent: ...


class TaskRepository(Protocol):
    async def create(self, task: Task) -> Task: ...

    async def list_open(self, *, household_id: str) -> list[Task]: ...

    async def set_status(self, *, household_id: str, task_id: str, status: TaskStatus) -> Task: ...


class ConversationRepository(Protocol):
    async def append(
        self,
        *,
        household_id: str,
        role: str,
        message: str,
        language: str,
        created_at: datetime,
    ) -> str: ...
