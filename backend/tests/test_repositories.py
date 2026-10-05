from datetime import datetime, timezone

import pytest

from app.domain import Consent, ConsentType, Task, TaskStatus
from app.memory_repositories import (
    InMemoryConsentRepository,
    InMemoryConversationRepository,
    InMemoryTaskRepository,
)


@pytest.mark.asyncio
async def test_consent_repository_is_keyed_by_household_and_type():
    repo = InMemoryConsentRepository()
    consent = Consent(
        household_id="h1",
        consent_type=ConsentType.MEMORY,
        granted=True,
        recorded_at=datetime.now(timezone.utc),
    )
    await repo.save(consent)

    assert await repo.get(household_id="h1", consent_type=ConsentType.MEMORY) == consent
    assert await repo.get(household_id="h2", consent_type=ConsentType.MEMORY) is None


@pytest.mark.asyncio
async def test_task_repository_isolates_households():
    repo = InMemoryTaskRepository()
    await repo.create(Task(household_id="h1", title="Income certificate"))
    await repo.create(Task(household_id="h2", title="Identity proof"))

    tasks = await repo.list_open(household_id="h1")
    assert [task.title for task in tasks] == ["Income certificate"]


@pytest.mark.asyncio
async def test_task_status_update_rejects_cross_household_access():
    repo = InMemoryTaskRepository()
    await repo.create(Task(household_id="h1", title="Call back"))

    with pytest.raises(KeyError, match="task_not_found"):
        await repo.set_status(
            household_id="h2",
            task_id="task-1",
            status=TaskStatus.COMPLETED,
        )


@pytest.mark.asyncio
async def test_conversation_repository_keeps_language_and_timestamp():
    repo = InMemoryConversationRepository()
    timestamp = datetime.now(timezone.utc)

    message_id = await repo.append(
        household_id="h1",
        role="user",
        message="Namaste",
        language="hi",
        created_at=timestamp,
    )

    assert message_id == "message-1"
    assert repo.messages[0]["language"] == "hi"
    assert repo.messages[0]["created_at"] == timestamp
