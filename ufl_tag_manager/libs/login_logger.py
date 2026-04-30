#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Logs user logins to a JSON file on the server.
- Captures: username + timestamp
- Deduplicates: one entry per user per day (won't flood the file)
- Size control: keeps only the last MAX_ENTRIES entries
Log file location: <app_root>/login_logs.json
"""

import os
import json
from datetime import datetime

ROOT       = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_FILE   = os.path.join(ROOT, "login_logs.json")
MAX_ENTRIES = 500  # keep last 500 login entries — older ones get dropped


def log_user_login(username: str) -> None:
    """
    Append a login entry for the given username if they haven't
    been logged today already.
    """
    try:
        _log(username)
    except Exception:
        pass  # logging must never break the app


def _log(username: str) -> None:
    username = (username or "").strip()
    if not username or username == "unknown":
        return

    today   = datetime.now().date().isoformat()   
    now_iso = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

    logs = _read_logs()

    # Deduplicate — skip if this user already has an entry for today
    already_logged = any(
        entry.get("username") == username and
        str(entry.get("timestamp", "")).startswith(today)
        for entry in logs
    )

    if already_logged:
        return

    logs.append({"username": username, "timestamp": now_iso})
    _write_logs(logs)


def _read_logs() -> list:
    """Read and return the log list. Returns [] if file missing or corrupt."""
    if not os.path.exists(LOG_FILE):
        return []

    try:
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data if isinstance(data, list) else []
    except (json.JSONDecodeError, OSError):
        return []


def _write_logs(logs: list) -> None:
 
    if len(logs) > MAX_ENTRIES:
        logs = logs[-MAX_ENTRIES:]  # drop oldest, keep newest 500

    with open(LOG_FILE, "w", encoding="utf-8") as f:
        json.dump(logs, f, indent=2)