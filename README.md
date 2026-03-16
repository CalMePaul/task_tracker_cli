# CLI Task Tracker

A small Python command-line app for managing tasks stored in JSON.

## Features

- Add tasks
- Update task descriptions
- Mark tasks as `todo`, `in-progress`, or `done`
- Delete tasks
- List all tasks

## Requirements

- Python 3.10+

## Setup

Create and activate a virtual environment, then install your tooling:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install pytest
```

## Usage

Run commands from the project root:

```powershell
python src/task_tracker.py --help
python src/task_tracker.py add "Buy milk"
python src/task_tracker.py update 1 "Buy oat milk"
python src/task_tracker.py mark 1 done
python src/task_tracker.py list
python src/task_tracker.py delete 1
```

Use `--help` to see the available commands and arguments:

```powershell
python src/task_tracker.py --help
python src/task_tracker.py mark --help
```

Example `list` output:

```text
1: Buy milk (todo)
2: Ship code (done)
```

## Testing

Run the test suite with:

```powershell
$env:PYTHONPATH="src"
python -m pytest -q src/test_task_manager.py
```

Temporary test files are created under `test_tmp/` and ignored by git.

## Documentation

- CLI reference: [docs/cli.md](/d:/Code/cli_task_tracker/docs/cli.md)
- Contribution guide: [CONTRIBUTING.md](/d:/Code/cli_task_tracker/CONTRIBUTING.md)
- License copy: [docs/LICENSE.md](/d:/Code/cli_task_tracker/LICENSE)
