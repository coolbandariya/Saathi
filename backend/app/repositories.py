from .domain import MemoryStore, Task

class InMemoryMemoryStore(MemoryStore):
    def __init__(self) -> None:
        self._tasks: dict[str, Task] = {}

    def get_tasks(self, household_id: str) -> list[Task]:
        return [task for task in self._tasks.values() if task.household_id == household_id]

    def create_task(self, task: Task) -> Task:
        if not task.household_id:
            raise ValueError("household_id is required")
        self._tasks[task.id] = task
        return task

    def complete_task(self, household_id: str, task_id: str) -> Task | None:
        task = self._tasks.get(task_id)
        if task is None or task.household_id != household_id:
            return None
        updated = task.model_copy(update={"status": "completed"})
        self._tasks[task_id] = updated
        return updated
