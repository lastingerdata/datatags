#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
import cgi
import cgitb
import urllib.parse
import time
from html import escape

cgitb.enable()

from jinja2 import Environment, FileSystemLoader, select_autoescape
from env_config import api_url, get_api_key, safe_request, get_base_path

BASE_PATH = get_base_path()
EXT = ".py"

ROOT = os.path.dirname(os.path.abspath(__file__))
TEMPLATES = os.path.join(ROOT, "templates")

env = Environment(
    loader=FileSystemLoader(TEMPLATES),
    autoescape=select_autoescape(["html", "xml"])
)

def print_headers(content_type="text/html; charset=utf-8", status=None, extra=None):
    if status:
        print(f"Status: {status}")
    print(f"Content-Type: {content_type}")
    if extra:
        for k, v in extra.items():
            print(f"{k}: {v}")
    print()
    
def redirect_with_messages(location_path, messages, extra_qs=None):
    qs = []
    for cat, msg in messages:
        qs.append(("c", cat))
        qs.append(("m", msg))
    if extra_qs:
        for k, v in extra_qs.items():
            if v is None:
                continue
            qs.append((k, v))
    qs.append(("_t", str(int(time.time() * 1000))))
    loc = f"{location_path}?{urllib.parse.urlencode(qs, doseq=True)}"
    print_headers(
        status="303 See Other",
        extra={
            "Location": loc,
            "Cache-Control": "no-store, no-cache, must-revalidate, max-age=0",
            "Pragma": "no-cache",
            "Expires": "0"
        }
    )
    print(f'<html><head><meta http-equiv="refresh" content="0;url={loc}"></head><body>Redirecting...</body></html>')
    sys.stdout.flush()
    sys.exit(0)

def get_qs_dict():
    raw = os.environ.get("QUERY_STRING", "")
    return dict(urllib.parse.parse_qsl(raw, keep_blank_values=True))

def get_param(fs, name, default=""):
    if name in fs:
        return fs.getfirst(name, default)
    return get_qs_dict().get(name, default)

def get_param_list(fs, name):
    if name in fs:
        return fs.getlist(name)
    return []

def api_headers():
    key = get_api_key()
    return {
        "Accept": "application/json",
        "ApiKey": key,
        "X-API-Key": key,
    }

def api_get_section_tags(params):
    params = dict(params or {})
    params["format"] = "json"
    qs = urllib.parse.urlencode(params, doseq=True)
    url = api_url("/section_tags_inserts")
    if qs:
        url = f"{url}?{qs}"

    resp = safe_request(url, method="GET", headers=api_headers(), verify=False)
    if isinstance(resp, dict):
        raise RuntimeError(resp.get("error", "Unknown error from backend"))

    try:
        data = resp.json()
    except Exception:
        text = getattr(resp, "text", "")
        raise RuntimeError("Non-JSON response from /section_tags_inserts: " + text[:300])

    if isinstance(data, dict) and not data.get("ok", True):
        raise RuntimeError(data.get("error", "Backend indicated failure"))

    return data

def api_map_tag_to_sections(tag_entry_id, selected_pairs, user):
    payload = {
        "format": "json",
        "map": "1",
        "tag_entry_id": str(tag_entry_id),
        "user": user or "",
        "selected_courses": selected_pairs,
    }

    url = api_url("/section_tags_inserts")
    resp = safe_request(url, method="POST", headers=api_headers(), data=payload, verify=False)

    if isinstance(resp, dict):
        return False, resp.get("error", "Unknown error from backend"), None, None

    try:
        data = resp.json()
    except Exception:
        text = getattr(resp, "text", "")
        return False, "Invalid JSON from backend: " + text[:200], None, None

    ok = bool(data.get("ok"))
    err = data.get("error")
    warning = data.get("warning")
    tag_label = data.get("tag_label")
    return ok, err, warning, tag_label

def build_url_for(name, **kw):
    route_map = {
        "tags_index":           f"{BASE_PATH}/tags_index{EXT}",
        "section_tags_inserts": f"{BASE_PATH}/section_tags_inserts{EXT}",
    }
    base = route_map.get(name, f"{BASE_PATH}/{name}{EXT}")
    if kw:
        return base + "?" + urllib.parse.urlencode(kw, doseq=True)
    return base

def section_tags_inserts():
    fs = cgi.FieldStorage()
    method = os.environ.get("REQUEST_METHOD", "GET").upper()
    qs_all = urllib.parse.parse_qs(os.environ.get("QUERY_STRING", ""), keep_blank_values=True)

    search           = get_param(fs, "search", "").strip().lower()
    wild_card        = get_param(fs, "wild_card", "").strip().lower()
    search_course    = get_param(fs, "search_course", "").strip().lower()
    wild_card_course = get_param(fs, "wild_card_course", "").strip().lower()
    start_date       = get_param(fs, "start_date", "").strip()
    end_date         = get_param(fs, "end_date", "").strip()
    department       = get_param(fs, "department", "").strip()
    term             = get_param(fs, "term", "").strip()
    tagged_status    = get_param(fs, "tagged_status", "").strip()
    page_str         = get_param(fs, "page", "1").strip()
    per_page_str     = get_param(fs, "per_page", "200").strip()

    try:
        page = int(page_str)
        if page < 1:
            page = 1
    except ValueError:
        page = 1

    try:
        per_page_val = int(per_page_str)
        if per_page_val not in [10, 25, 50, 100, 200]:
            per_page_val = 200
    except ValueError:
        per_page_val = 200

    tag_entry_id = get_param(fs, "tag_entry_id", "").strip()

    if method == "POST" and ("map" in fs or get_param(fs, "map", "") == "1"):
        selected = get_param_list(fs, "selected_courses")
        user = get_param(fs, "user", "").strip()

        keep_qs = {
            "tag_entry_id": tag_entry_id or "",
            "search": search,
            "wild_card": wild_card,
            "search_course": search_course,
            "wild_card_course": wild_card_course,
            "start_date": start_date,
            "end_date": end_date,
            "department": department,
            "term": term,
            "tagged_status": tagged_status,
            "page": str(page),
            "per_page": str(per_page_val),
        }

        if not tag_entry_id:
            return redirect_with_messages(
                f"{BASE_PATH}/section_tags_inserts{EXT}",
                [("danger", "Please select a tag to apply.")],
                keep_qs,
            )
        if not selected:
            return redirect_with_messages(
                f"{BASE_PATH}/section_tags_inserts{EXT}",
                [("danger", "Please select at least one course.")],
                keep_qs,
            )

        ok, err, warning, tag_label = api_map_tag_to_sections(tag_entry_id, selected, user)

        if not ok:
            msg = err or "Failed to apply tag."
            return redirect_with_messages(
                f"{BASE_PATH}/section_tags_inserts{EXT}",
                [("danger", msg)],
                keep_qs,
            )

        if warning:
            return redirect_with_messages(
                f"{BASE_PATH}/section_tags_inserts{EXT}",
                [("warning", warning)],
                keep_qs,
            )

        if tag_label:
            return redirect_with_messages(
                f"{BASE_PATH}/section_tags_inserts{EXT}",
                [("success", f'Tag "{tag_label}" is added to the selected course(s).')],
                keep_qs,
            )

        return redirect_with_messages(
            f"{BASE_PATH}/section_tags_inserts{EXT}",
            [("success", "Tag applied to selected courses")],
            keep_qs,
        )

    try:
        params = dict(
            search=search,
            search_course=search_course,
            tag_entry_id=tag_entry_id,
            start_date=start_date,
            end_date=end_date,
            department=department,
            term=term,
            tagged_status=tagged_status,
            wild_card=wild_card,
            wild_card_course=wild_card_course,
            page=str(page),
            per_page=str(per_page_val),
        )
        data = api_get_section_tags(params)

        tag_values  = data.get("tag_values", []) or []
        courses     = data.get("courses", []) or []
        total_count = int(data.get("total_results", data.get("total_count", 0)) or 0)
        per_page    = int(data.get("per_page", per_page_val) or per_page_val)
        total_pages = int(data.get("total_pages", 1) or 1)

    except Exception as e:
        tag_values = []
        courses = []
        total_count = 0
        per_page = per_page_val
        total_pages = 1
        qs_all.setdefault("c", []).append("danger")
        qs_all.setdefault("m", []).append(f"Failed to load data: {escape(str(e))}")

    deleted_flag = get_qs_dict().get("deleted", "")
    if deleted_flag == "1":
        qs_all.setdefault("c", []).append("success")
        qs_all.setdefault("m", []).append("Tag value deleted")
    elif deleted_flag == "0":
        qs_all.setdefault("c", []).append("danger")
        qs_all.setdefault("m", []).append("Cannot delete tag value (likely has associated values)")

    cats = qs_all.get("c", [])
    msgs = qs_all.get("m", [])
    flashed = []
    if isinstance(cats, str):
        cats = [cats]
    if isinstance(msgs, str):
        msgs = [msgs]
    for cat, msg in zip(cats, msgs):
        flashed.append((cat, msg))

    template = env.get_template("section_tags_inserts.html")
    html = template.render(
        get_flashed_messages=lambda with_categories=False:
            flashed if with_categories else [m for _, m in flashed],
        base_path=BASE_PATH,
        ext=EXT,
        tag_values=tag_values,
        courses=courses,
        tag_entry_id=tag_entry_id,
        search=search,
        search_course=search_course,
        wild_card=wild_card,
        wild_card_course=wild_card_course,
        start_date=start_date,
        end_date=end_date,
        department=department,
        term=term,
        page_name='section_tags_inserts',
        tagged_status=tagged_status,
        page=page,
        per_page=per_page_val,
        total_results=total_count,
        total_pages=total_pages,
        url_for=lambda name, **kw: build_url_for(name, **kw),
    )

    cache_headers = {
        "Cache-Control": "no-store, no-cache, must-revalidate, max-age=0",
        "Pragma": "no-cache",
        "Expires": "0"
    }
    print_headers(extra=cache_headers)
    sys.stdout.write(html)

if __name__ == "__main__":
    try:
        section_tags_inserts()
    except Exception as e:
        print_headers()
        sys.stdout.write(f"<h3>Unhandled error</h3><pre>{escape(str(e))}</pre>")
