# Contributing

## Development Setup

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install pytest pylint black
```

## Project Layout

- `src/task_tracker.py`: CLI entry point and argument parsing
- `src/task_manager.py`: task storage logic
- `src/test_task_manager.py`: tests for task operations
- `src/tasks.json`: local task data file
- `docs/`: project documentation

## Running Tests

Use the local source directory when running tests:

```powershell
$env:PYTHONPATH="src"
python -m pytest -q src/test_task_manager.py
```

Tests write temporary files to `test_tmp/`, which is ignored by git.

## Contribution Expectations

- Keep changes focused
- Add or update tests for behavior changes
- Preserve the current CLI command names unless the change is intentional
- Avoid committing local task data or temporary test files

## Style Notes

- Use clear function names
- Keep comments short and useful
- Prefer small, testable functions over large blocks of logic
