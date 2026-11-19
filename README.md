# Bug Tracker CLI

A small command-line bug tracker for developers, written in pure Python (no dependencies). Bugs are stored in a local `bugs.json` file.

## Usage

```bash
python tracker.py add "Login button not working" -s high
python tracker.py add "Typo on homepage" -s low
python tracker.py list
python tracker.py list --status open
python tracker.py start 1
python tracker.py close 1
```

Severities: `low`, `medium`, `high`, `critical`. Bugs are listed most severe first.

## Run tests

```bash
python -m unittest -v
```

## Concepts demonstrated
- CLI design with `argparse`
- JSON persistence
- Unit testing with `unittest`
- Basic issue-tracking workflow (open → in-progress → closed)
