import json
from pathlib import Path
from datetime import datetime

TASKS_FILE = Path(__file__).with_name("tasks.json")


def _load_tasks():
    """Load all the tasks from the tasks.json file (memory)."""
    with TASKS_FILE.open("r", encoding="utf-8") as file:
        return json.load(file)


def _save_tasks(tasks):
    """Save all the tasks to the tasks.json file (memory)."""
    with TASKS_FILE.open("w", encoding="utf-8") as file:
        return json.dump(tasks, file)


def add_task(description):
    """Add a task to the JSON file (tracker)."""
    tasks = _load_tasks()
    task_id = len(tasks) + 1

    tasks.append(
        {
            "id": task_id,
            "description": description,
            "status": "todo",
            "createdAt": str(datetime.now()),
            "updatedAt": str(datetime.now()),
        }
    )

    _save_tasks(tasks)


def update_task(task_id, description):
    """Add a task to the JSON file (tracker)."""
    tasks = _load_tasks()
    task_found = False  # Flag.

    for task in tasks:
        if task["id"] == task_id:
            tasks.append(
                {
                    "id": task_id,
                    "description": description,
                    "status": "todo",
                    "createdAt": task["createdAt"],
                    "updatedAt": str(datetime.now()),
                }
            )
            task_found = True

    if not task_found:
        raise ValueError(f"Task with id {task_id} not found.")

    _save_tasks(tasks)


def mark_task(task_id, status):
    """Change the status of a task."""
    tasks = _load_tasks()
    task_found = False  # Flag.

    for task in tasks:
        if task["id"] == task_id:
            tasks.append(
                {
                    "id": task_id,
                    "description": task["description"],
                    "status": status,
                    "createdAt": task["createdAt"],
                    "updatedAt": str(datetime.now()),
                }
            )
            task_found = True

    if not task_found:
        raise ValueError(f"Task with id {task_id} not found.")

    _save_tasks(tasks)


def delete_task(task_id):
    """Delete a task by id."""
    tasks = _load_tasks()
    task_found = False  # Flag.

    for task in tasks:
        if task["id"] == task_id:
            tasks.remove(task)
            task_found = True

    if not task_found:
        raise ValueError(f"Task with id {task_id} not found.")

    _save_tasks(tasks)
