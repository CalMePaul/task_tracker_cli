# CLI Reference

## Command Format

Run the CLI from the project root:

```powershell
python src/task_tracker.py <command> [arguments]
```

To view the built-in help:

```powershell
python src/task_tracker.py --help
```

## Commands

### `--help`

Show the available commands or the help for a specific command.

```powershell
python src/task_tracker.py --help
python src/task_tracker.py add --help
python src/task_tracker.py mark --help
```

### `add`

Add a new task.

```powershell
python src/task_tracker.py add "Buy milk"
```

### `update`

Update an existing task description by id.

```powershell
python src/task_tracker.py update 1 "Buy oat milk"
```

### `mark`

Change a task status.

Allowed statuses:

- `todo`
- `in-progress`
- `done`

```powershell
python src/task_tracker.py mark 1 done
python src/task_tracker.py mark 2 in-progress
```

### `delete`

Delete a task by id.

```powershell
python src/task_tracker.py delete 1
```

### `list`

Print all stored tasks, one per line.

```powershell
python src/task_tracker.py list
```

Example output:

```text
1: Buy milk (todo)
2: Ship code (done)
```

## Errors

If a task id does not exist, the CLI exits with status code `1` and prints:

```text
Error: Task with id <id> not found.
```

## Data Storage

Task data is stored in:

- `src/tasks.json`
