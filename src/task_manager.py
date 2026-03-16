import json
from pathlib import Path
from datetime import datetime

TASKS_FILE = Path(__file__).with_name("tasks.json")


def _load_tasks_file():
    """Load all the tasks from the tasks.json file (memory)."""
    # No try-except architecture because an error in JSON must stop the program (memory error).
    with TASKS_FILE.open("r", encoding="utf-8") as file:
        return json.load(file)


def _save_tasks_file(tasks):
    """Save all the tasks to the tasks.json file (memory)."""
    with TASKS_FILE.open("w", encoding="utf-8") as file:
        return json.dump(tasks, file, indent=4)


def add_task(description):
    """Add a task to the JSON file (tracker)."""
    tasks_dict = _load_tasks_file()
    task_id = tasks_dict["next_id"]

    tasks_dict["tasks"].append(
        {
            "id": task_id,
            "description": description,
            "status": "todo",
            "createdAt": str(datetime.now()),
            "updatedAt": str(datetime.now()),
        }
    )
    tasks_dict["next_id"] += 1

    _save_tasks_file(tasks_dict)


def update_task(task_id, description):
    """Add a task to the JSON file (tracker)."""
    tasks_dict = _load_tasks_file()
    task_found = False  # Flag.

    for task in tasks_dict["tasks"]:
        if task["id"] == task_id:
            task["description"] = description
            task["updatedAt"] = str(datetime.now())

            task_found = True

    if not task_found:
        raise ValueError(f"Task with id {task_id} not found.")

    _save_tasks_file(tasks_dict)


def mark_task(task_id, status):
    """Change the status of a task."""
    tasks_dict = _load_tasks_file()
    task_found = False  # Flag.

    for task in tasks_dict["tasks"]:
        if task["id"] == task_id:
            task["status"] = status
            task["updatedAt"] = str(datetime.now())

            task_found = True

    if not task_found:
        raise ValueError(f"Task with id {task_id} not found.")

    _save_tasks_file(tasks_dict)


def delete_task(task_id):
    """Delete a task by id."""
    tasks_dict = _load_tasks_file()
    task_found = False  # Flag.

    for task in tasks_dict["tasks"]:
        if task["id"] == task_id:
            tasks_dict["tasks"].remove(task)
            task_found = True

    if not task_found:
        raise ValueError(f"Task with id {task_id} not found.")

    _save_tasks_file(tasks_dict)


def list_tasks():
    """List all tasks."""
    tasks_dict = _load_tasks_file()

    for task in tasks_dict["tasks"]:
        # Add a newline after each task so every task is shown on its own line.
        print(f"{task['id']}: {task['description']} ({task["status"]})", end="\n")
