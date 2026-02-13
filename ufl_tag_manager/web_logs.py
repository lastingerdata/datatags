#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import cgitb
import traceback
from html import escape
from time import time
import urllib.parse
import json
import heapq

import requests
from jinja2 import Environment, FileSystemLoader, select_autoescape
from env_config import get_base_path

cgitb.enable()

BASE_PATH = get_base_path()
EXT = ".py"

WEB_LOGS_URL = "https://compute.lastinger.center.ufl.edu/web_logs"
WEB_LOGS_API_KEY = "596fa395d7a9072c06207b119ec415164487d50a37f904d08542305466a80fce"

CACHE_TTL_SECONDS = 300
DEFAULT_LIMIT = 50

CACHE_FILE = "/tmp/ufl_web_logs_cache.json"
LOCK_FILE = "/tmp/ufl_web_logs_cache.lock"

ROOT = os.path.dirname(os.path.abspath(__file__))
TEMPLATES = os.path.join(ROOT, "templates")

env = Environment(
    loader=FileSystemLoader(TEMPLATES),
    autoescape=select_autoescape(["html", "xml"])
)

def _read_file_cache():
    try:
        if not os.path.exists(CACHE_FILE):
            return None
        with open(CACHE_FILE, "r", encoding="utf-8") as f:
            obj = json.load(f)
        if not isinstance(obj, dict):
            return None
        if "ts" not in obj or "entries" not in obj or "meta" not in obj:
            return None
        if not isinstance(obj.get("entries"), list) or not isinstance(obj.get("meta"), dict):
            return None
        return obj
    except Exception:
        return None

def _write_file_cache(ts, entries, meta):
    try:
        tmp = CACHE_FILE + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump({"ts": ts, "entries": entries, "meta": meta}, f)
        os.replace(tmp, CACHE_FILE)
    except Exception:
        pass

def _acquire_lock(max_wait_seconds=1.5):
    start = time()
    while True:
        try:
            fd = os.open(LOCK_FILE, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
            os.write(fd, str(os.getpid()).encode("utf-8"))
            os.close(fd)
            return True
        except FileExistsError:
            if (time() - start) > max_wait_seconds:
                return False
        except Exception:
            return False

def _release_lock():
    try:
        if os.path.exists(LOCK_FILE):
            os.remove(LOCK_FILE)
    except Exception:
        pass

def fetch_web_logs_or_error():
    headers = {"Accept": "application/json", "ApiKey": WEB_LOGS_API_KEY}

    try:
        with requests.Session() as s:
            resp = s.get(
                WEB_LOGS_URL,
                headers=headers,
                timeout=(5, 25),
                verify=False,
                proxies={}
            )
    except Exception as e:
        return [], {"ok": False, "status": None, "error": f"Request error: {e}"}

    status = resp.status_code
    text = resp.text or ""

    try:
        data = resp.json()
    except Exception as e:
        return [], {"ok": False, "status": status, "error": f"JSON parse error: {e} | body: {text[:300]}"}

    if isinstance(data, dict) and data.get("error"):
        return [], {"ok": False, "status": status, "error": str(data.get("error"))}

    if isinstance(data, list):
        logs = [x for x in data if isinstance(x, dict)]
        return logs, {"ok": True, "status": status, "count": len(logs)}

    if isinstance(data, dict) and isinstance(data.get("logs"), list):
        logs = [x for x in data["logs"] if isinstance(x, dict)]
        return logs, {"ok": True, "status": status, "count": len(logs)}

    return [], {"ok": False, "status": status, "error": "Unexpected response format"}

def get_cached_or_fetch():
    now = time()
    cached = _read_file_cache()
    if cached:
        age = now - float(cached.get("ts") or 0)
        if age < CACHE_TTL_SECONDS:
            return cached.get("entries") or [], cached.get("meta") or {}, True

    got_lock = _acquire_lock()
    try:
        cached2 = _read_file_cache()
        if cached2:
            age2 = now - float(cached2.get("ts") or 0)
            if age2 < CACHE_TTL_SECONDS:
                return cached2.get("entries") or [], cached2.get("meta") or {}, True

        entries, meta = fetch_web_logs_or_error()
        _write_file_cache(now, entries, meta)
        return entries, meta, False
    finally:
        if got_lock:
            _release_lock()

def get_limit_from_qs():
    qs = urllib.parse.parse_qs(os.environ.get("QUERY_STRING", ""))
    raw = (qs.get("limit", [str(DEFAULT_LIMIT)])[0] or "").strip().lower()

    if raw in ("all", "max"):
        return None, "all"

    try:
        n = int(raw)
        if n <= 0:
            return DEFAULT_LIMIT, str(DEFAULT_LIMIT)
        return n, str(n)
    except Exception:
        return DEFAULT_LIMIT, str(DEFAULT_LIMIT)

def filter_messages(msgs):
    if not isinstance(msgs, list):
        msgs = [str(msgs)]

    out = []
    for m in msgs:
        if not isinstance(m, str):
            continue
        s = m.strip()
        if s == "Valid Key in use:":
            continue
        if s.lower().startswith("api_key:"):
            continue
        if s == "ACCESSOK:":
            continue
        out.append(m)
    return out

def build_rows(entries):
    rows = []
    for e in entries:
        rows.append({
            "session": e.get("session", "-"),
            "start_time": e.get("start_time", "-"),
            "messages": filter_messages(e.get("messages") or [])
        })
    return rows

def _start_time_key(e):
    return str(e.get("start_time") or "")

def main():
    try:
        limit, limit_label = get_limit_from_qs()
        entries, meta, cache_hit = get_cached_or_fetch()

        messages = []
        if not meta.get("ok"):
            messages.append(("danger", f"web_logs fetch failed (status={meta.get('status')}): {meta.get('error')}"))

        total = len(entries)

        if total == 0:
            chosen = []
        else:
            if limit is None:
                chosen = sorted(entries, key=_start_time_key, reverse=True)
            else:
                show_n = min(limit, total)
                chosen = heapq.nlargest(show_n, entries, key=_start_time_key)
                chosen = sorted(chosen, key=_start_time_key, reverse=True)

        showing = len(chosen)
        rows = build_rows(chosen)

        print("Content-Type: text/html; charset=utf-8")
        print()

        print(env.get_template("web_logs.html").render(
            base_path=BASE_PATH,
            ext=EXT,
            rows=rows,
            messages=messages,
            page_name="web_logs",
            cache_hit=cache_hit,
            cache_ttl=CACHE_TTL_SECONDS,
            total=total,
            showing=showing,
            current_limit=limit_label
        ))

    except Exception:
        print("Content-Type: text/html; charset=utf-8")
        print()
        print("<h1>Web Logs crashed</h1>")
        print("<pre>")
        print(escape(traceback.format_exc()))
        print("</pre>")

if __name__ == "__main__":
    main()
