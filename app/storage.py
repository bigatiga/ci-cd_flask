from datetime import datetime

_tasks = {}
_counter = 1


def _next_id():
    global _counter
    tid = _counter
    _counter += 1
    return tid


def reset():
    """Reset storage — used in tests."""
    global _tasks, _counter
    _tasks = {}
    _counter = 1


def get_all():
    return list(_tasks.values())


def get_by_id(task_id: int):
    return _tasks.get(task_id)


def create(title: str, description: str = "") -> dict:
    if not title or not title.strip():
        raise ValueError("Title is required")
    task = {
        "id": _next_id(),
        "title": title.strip(),
        "description": description.strip(),
        "done": False,
        "created_at": datetime.utcnow().isoformat(),
    }
    _tasks[task["id"]] = task
    return task


def update(task_id: int, data: dict) -> dict:
    task = _tasks.get(task_id)
    if task is None:
        raise KeyError(task_id)
    if "title" in data:
        if not data["title"] or not data["title"].strip():
            raise ValueError("Title cannot be empty")
        task["title"] = data["title"].strip()
    if "description" in data:
        task["description"] = data["description"].strip()
    if "done" in data:
        task["done"] = bool(data["done"])
    return task


def delete(task_id: int) -> bool:
    if task_id not in _tasks:
        raise KeyError(task_id)
    del _tasks[task_id]
    return True
