#!/usr/bin/env python3
"""Bug Tracker CLI - a tiny issue tracker for developers (JSON storage)."""
import argparse
import json
import os
from datetime import datetime

DB_FILE = os.environ.get("BUG_DB", "bugs.json")
SEVERITIES = ["low", "medium", "high", "critical"]


def load(db=None):
    path = db or DB_FILE
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save(bugs, db=None):
    with open(db or DB_FILE, "w", encoding="utf-8") as f:
        json.dump(bugs, f, indent=2)


def add_bug(title, severity="medium", db=None):
    if severity not in SEVERITIES:
        raise ValueError(f"severity must be one of {SEVERITIES}")
    bugs = load(db)
    bug = {
        "id": max((b["id"] for b in bugs), default=0) + 1,
        "title": title,
        "severity": severity,
        "status": "open",
        "created": datetime.now().strftime("%Y-%m-%d %H:%M"),
    }
    bugs.append(bug)
    save(bugs, db)
    return bug


def set_status(bug_id, status, db=None):
    bugs = load(db)
    for b in bugs:
        if b["id"] == bug_id:
            b["status"] = status
            save(bugs, db)
            return b
    raise KeyError(f"Bug #{bug_id} not found")


def list_bugs(status=None, db=None):
    bugs = load(db)
    if status:
        bugs = [b for b in bugs if b["status"] == status]
    return sorted(bugs, key=lambda b: -SEVERITIES.index(b["severity"]))


def main():
    p = argparse.ArgumentParser(description="Simple Bug Tracker")
    sub = p.add_subparsers(dest="cmd", required=True)

    a = sub.add_parser("add", help="report a new bug")
    a.add_argument("title")
    a.add_argument("-s", "--severity", default="medium", choices=SEVERITIES)

    l = sub.add_parser("list", help="list bugs")
    l.add_argument("--status", choices=["open", "in-progress", "closed"])

    for name in ("start", "close"):
        c = sub.add_parser(name, help=f"{name} a bug")
        c.add_argument("id", type=int)

    args = p.parse_args()
    try:
        if args.cmd == "add":
            b = add_bug(args.title, args.severity)
            print(f"Added bug #{b['id']}: {b['title']} [{b['severity']}]")
        elif args.cmd == "list":
            for b in list_bugs(args.status):
                print(f"#{b['id']:<3} [{b['severity']:<8}] {b['status']:<11} {b['title']}")
        elif args.cmd == "start":
            print(f"Bug #{set_status(args.id, 'in-progress')['id']} is in progress")
        elif args.cmd == "close":
            print(f"Bug #{set_status(args.id, 'closed')['id']} closed")
    except (ValueError, KeyError) as e:
        print(f"Error: {e}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
