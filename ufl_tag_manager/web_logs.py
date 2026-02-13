#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
import cgitb
import traceback
import urllib.parse
from html import escape
from time import time
import heapq

cgitb.enable()

from jinja2 import Environment, FileSystemLoader, select_autoescape
from env_config import safe_request, get_base_path, get_api_key

BASE_PATH = get_base_path()
EXT = ".py"

WEB_LOGS_URL = "https://compute.lastinger.center.ufl.edu/web_logs"

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


def parse_json_lenient(resp):
    if isinstance(resp, (dict, list)):
        return resp
    try:
        return resp.json()
    except Exception:
        pass

    text = (getattr(resp, "text", "") or "").lstrip()
    if text.lower().startswith("pretty-print"):
        text = text.split("\n", 1)[1] if "\n" in text else ""

    start_obj = text.find("{")
    start_arr = text.find("[")
    starts = [i for i in (start_obj, start_arr) if i != -1]
    if not starts:
        snippet = text[:200].replace("<", "&lt;").replace(">", "&gt;")
        raise RuntimeError(f"web_logs endpoint did not return JSON. Snippet: {snippet}")

    return json.loads(text[min(starts):])


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


def _make_headers():
    headers = {"Accept": "application/json"}
    api_key = get_api_key(1)
    if api_key:
        headers["ApiKey"] = api_key
    return headers


def fetch_web_logs_or_error():
    headers = _make_headers()

    resp = safe_request(WEB_LOGS_URL, headers=headers, verify=False)

    if isinstance(resp, dict) and resp.get("error"):
        return [], {"ok": False, "status": None, "error": str(resp.get("error"))}

    status = getattr(resp, "status_code", None)

    try:
        data = parse_json_lenient(resp)
    except Exception as e:
        txt = (getattr(resp, "text", "") or "")[:300]
        return [], {"ok": False, "status": status, "error": f"{e} | body: {txt}"}

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
            showing=len(rows),
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
