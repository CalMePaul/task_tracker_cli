import json
from pathlib import Path
import pytest
import task_manager


@pytest.fixture
def temp_tasks_file(request, monkeypatch):
    """Create an isolated tasks file for each test case."""
    temp_root = Path(__file__).resolve().parent.parent / "test_tmp"
    temp_root.mkdir(exist_ok=True)

    # Keep each test case in its own folder so the JSON file stays isolated.
    tmp_file = temp_root / request.node.name
    tmp_file.mkdir(exist_ok=True)

    # Start each test from a clean JSON structure.
    temp_tasks_path = tmp_file / "tasks.json"
    temp_tasks_path.write_text(
        json.dumps({"next_id": 1, "tasks": []}),
        encoding="utf-8",
    )

    # Redirect task_manager reads and writes to the temporary file.
    monkeypatch.setattr(task_manager, "TASKS_FILE", temp_tasks_path)
    return temp_tasks_path


def read_tasks_data(tasks_file):
    """Load task data from the temporary JSON file."""
    with tasks_file.open("r", encoding="utf-8") as file:
        return json.load(file)


def write_tasks_data(tasks_file, data):
    """Seed the temporary JSON file with known task data."""
    with tasks_file.open("w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)


def test_add_task_creates_task_and_increments_next_id(temp_tasks_file):
    """Add a task and verify the persisted defaults and next id."""
    task_manager.add_task("Buy milk")

    data = read_tasks_data(temp_tasks_file)

    assert data["next_id"] == 2
    assert len(data["tasks"]) == 1
    assert data["tasks"][0]["id"] == 1
    assert data["tasks"][0]["description"] == "Buy milk"
    assert data["tasks"][0]["status"] == "todo"
    assert data["tasks"][0]["createdAt"]
    assert data["tasks"][0]["updatedAt"]


def test_update_task_changes_only_matching_task(temp_tasks_file):
    """Update one task without changing the other stored task."""
    # Use two tasks so the test proves only the matching id is changed.
    write_tasks_data(
        temp_tasks_file,
        {
            "next_id": 3,
            "tasks": [
                {
                    "id": 1,
                    "description": "Old description",
                    "status": "todo",
                    "createdAt": "2026-03-16 10:00:00",
                    "updatedAt": "2026-03-16 10:00:00",
                },
                {
                    "id": 2,
                    "description": "Leave me alone",
                    "status": "done",
                    "createdAt": "2026-03-16 11:00:00",
                    "updatedAt": "2026-03-16 11:00:00",
                },
            ],
        },
    )

    task_manager.update_task(1, "New description")

    data = read_tasks_data(temp_tasks_file)

    assert data["tasks"][0]["id"] == 1
    assert data["tasks"][0]["description"] == "New description"
    assert data["tasks"][0]["updatedAt"] != "2026-03-16 10:00:00"
    assert data["tasks"][1]["description"] == "Leave me alone"
    assert data["tasks"][1]["status"] == "done"


def test_update_task_raises_error_for_missing_id(temp_tasks_file):
    """Raise a ValueError and keep file contents unchanged for a bad id."""
    original_data = {
        "next_id": 2,
        "tasks": [
            {
                "id": 1,
                "description": "Existing task",
                "status": "todo",
                "createdAt": "2026-03-16 10:00:00",
                "updatedAt": "2026-03-16 10:00:00",
            }
        ],
    }
    write_tasks_data(temp_tasks_file, original_data)

    with pytest.raises(ValueError) as error:
        task_manager.update_task(99, "New description")

    data = read_tasks_data(temp_tasks_file)

    # The function should fail without mutating the stored data.
    assert str(error.value) == "Task with id 99 not found."
    assert data == original_data


def test_mark_task_changes_only_matching_task(temp_tasks_file):
    """Change one task status without affecting the other task."""
    # Keep a second task in the file to catch accidental broad updates.
    write_tasks_data(
        temp_tasks_file,
        {
            "next_id": 3,
            "tasks": [
                {
                    "id": 1,
                    "description": "Work in progress",
                    "status": "todo",
                    "createdAt": "2026-03-16 10:00:00",
                    "updatedAt": "2026-03-16 10:00:00",
                },
                {
                    "id": 2,
                    "description": "Already done",
                    "status": "done",
                    "createdAt": "2026-03-16 11:00:00",
                    "updatedAt": "2026-03-16 11:00:00",
                },
            ],
        },
    )

    task_manager.mark_task(1, "in-progress")

    data = read_tasks_data(temp_tasks_file)

    assert data["tasks"][0]["status"] == "in-progress"
    assert data["tasks"][0]["updatedAt"] != "2026-03-16 10:00:00"
    assert data["tasks"][1]["status"] == "done"
    assert data["tasks"][1]["description"] == "Already done"


def test_mark_task_raises_error_for_missing_id(temp_tasks_file):
    """Raise a ValueError and preserve task data for a missing id."""
    original_data = {
        "next_id": 2,
        "tasks": [
            {
                "id": 1,
                "description": "Existing task",
                "status": "todo",
                "createdAt": "2026-03-16 10:00:00",
                "updatedAt": "2026-03-16 10:00:00",
            }
        ],
    }
    write_tasks_data(temp_tasks_file, original_data)

    with pytest.raises(ValueError) as error:
        task_manager.mark_task(99, "done")

    data = read_tasks_data(temp_tasks_file)

    # A failed status change should not rewrite the JSON content.
    assert str(error.value) == "Task with id 99 not found."
    assert data == original_data


def test_delete_task_removes_only_matching_task(temp_tasks_file):
    """Delete one task and leave the remaining task untouched."""
    # Two tasks make it clear which record should survive the delete.
    write_tasks_data(
        temp_tasks_file,
        {
            "next_id": 3,
            "tasks": [
                {
                    "id": 1,
                    "description": "Delete me",
                    "status": "todo",
                    "createdAt": "2026-03-16 10:00:00",
                    "updatedAt": "2026-03-16 10:00:00",
                },
                {
                    "id": 2,
                    "description": "Keep me",
                    "status": "done",
                    "createdAt": "2026-03-16 11:00:00",
                    "updatedAt": "2026-03-16 11:00:00",
                },
            ],
        },
    )

    task_manager.delete_task(1)

    data = read_tasks_data(temp_tasks_file)

    assert len(data["tasks"]) == 1
    assert data["tasks"][0]["id"] == 2
    assert data["tasks"][0]["description"] == "Keep me"
    assert data["next_id"] == 3


def test_delete_task_raises_error_for_missing_id(temp_tasks_file):
    """Raise a ValueError and keep existing tasks when id is missing."""
    original_data = {
        "next_id": 2,
        "tasks": [
            {
                "id": 1,
                "description": "Existing task",
                "status": "todo",
                "createdAt": "2026-03-16 10:00:00",
                "updatedAt": "2026-03-16 10:00:00",
            }
        ],
    }
    write_tasks_data(temp_tasks_file, original_data)

    with pytest.raises(ValueError) as error:
        task_manager.delete_task(99)

    data = read_tasks_data(temp_tasks_file)

    # No task should be removed when the requested id does not exist.
    assert str(error.value) == "Task with id 99 not found."
    assert data == original_data


def test_list_tasks_prints_each_task_on_its_own_line(temp_tasks_file, capsys):
    """Print each stored task once without extra blank lines."""
    write_tasks_data(
        temp_tasks_file,
        {
            "next_id": 3,
            "tasks": [
                {
                    "id": 1,
                    "description": "Buy milk",
                    "status": "todo",
                    "createdAt": "2026-03-16 10:00:00",
                    "updatedAt": "2026-03-16 10:00:00",
                },
                {
                    "id": 2,
                    "description": "Ship code",
                    "status": "done",
                    "createdAt": "2026-03-16 11:00:00",
                    "updatedAt": "2026-03-16 11:00:00",
                },
            ],
        },
    )

    task_manager.list_tasks()

    # capsys collects printed output from the function during the test.
    captured = capsys.readouterr()

    # Each task should end with exactly one newline, with no blank line between tasks.
    assert captured.out == "1: Buy milk (todo)\n2: Ship code (done)\n"


def test_list_tasks_prints_nothing_when_no_tasks_exist(temp_tasks_file, capsys):
    """Leave stdout empty when there are no stored tasks."""
    task_manager.list_tasks()

    # Read everything that was printed so we can verify the command stayed silent.
    captured = capsys.readouterr()

    assert captured.out == ""
