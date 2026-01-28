#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import cgi
import cgitb
import traceback
import urllib.parse
import json
import requests

cgitb.enable()

from jinja2 import Environment, FileSystemLoader, select_autoescape
from env_config import api_url, get_api_key, safe_request, get_base_path, can_write

ROOT = os.path.dirname(os.path.abspath(__file__))
TEMPLATES = os.path.join(ROOT, "templates")
env = Environment(
    loader=FileSystemLoader(TEMPLATES),
    autoescape=select_autoescape(["html", "xml"])
)

BASE_PATH = get_base_path()
EXT = ".py"


def print_headers(content_type="text/html; charset=utf-8", status=None, extra=None):
    if status:
        print(f"Status: {status}")
    print(f"Content-Type: {content_type}")
    if extra:
        for k, v in extra.items():
            print(f"{k}: {v}")
    print()


def redirect_with_messages(messages, extra_qs=None):
    import time
    pairs = [("m", f"{c}:{t}") for c, t in messages]
    pairs.append(("_t", str(int(time.time() * 1000))))
    if extra_qs:
        for k, v in extra_qs.items():
            if v is not None and v != "":
                pairs.append((k, str(v)))
    qs = urllib.parse.urlencode(pairs)
    location = f"{BASE_PATH}/tag_values{EXT}" + (f"?{qs}" if qs else "")
    print_headers(
        status="303 See Other",
        extra={
            "Cache-Control": "no-store, no-cache, must-revalidate, max-age=0",
            "Pragma": "no-cache",
            "Location": location
        }
    )
    print(
        f'<html><head><meta http-equiv="refresh" content="0;url={location}"></head>'
        f'<body>Redirecting...</body></html>'
    )
    sys.stdout.flush()


def parse_messages_from_qs():
    messages = []
    qs = os.environ.get("QUERY_STRING", "")
    if not qs:
        return messages
    for v in urllib.parse.parse_qs(qs, keep_blank_values=True).get("m", []):
        if ":" in v:
            c, t = v.split(":", 1)
            messages.append((c, t))
    return messages


def get_qs_param(name, default=""):
    qd = urllib.parse.parse_qs(os.environ.get("QUERY_STRING", ""), keep_blank_values=True)
    return (qd.get(name, [default])[0] or default)


def _read_text(resp, limit=800):
    try:
        return (getattr(resp, "text", "") or "")[:limit]
    except Exception:
        return ""


def fetch_tags_list():
    headers = {"Accept": "application/json", "ApiKey": get_api_key()}
    resp = safe_request(api_url("/tags?format=json"), headers=headers, verify=False)

    if isinstance(resp, dict):
        raise RuntimeError(resp.get("error", "API Error"))

    sc = getattr(resp, "status_code", 200)
    if not (200 <= sc < 300):
        raise RuntimeError(f"Backend {sc}: {_read_text(resp)}")

    ctype = (resp.headers.get("Content-Type") or "").lower()
    if "application/json" not in ctype:
        raise RuntimeError(
            f"Backend did not return JSON (Content-Type: {ctype}). Body: {_read_text(resp)}"
        )

    data = resp.json()
    tags = data.get("data", []) if isinstance(data, dict) else data

    if not isinstance(tags, list):
        preview = json.dumps(data, default=str)[:400]
        raise RuntimeError(f"Unexpected JSON for tags. Preview: {preview}")

    return tags


def fetch_values_for_tag(tag_id):
    import time
    cache_buster = int(time.time() * 1000)
    headers = {
        "Accept": "application/json",
        "ApiKey": get_api_key(),
        "Cache-Control": "no-cache, no-store, must-revalidate",
        "Pragma": "no-cache"
    }
    url = api_url(
        f"/tag_values?tag_id={urllib.parse.quote_plus(str(tag_id))}&format=json&_t={cache_buster}"
    )
    resp = safe_request(url, headers=headers, verify=False)

    if isinstance(resp, dict):
        raise RuntimeError(resp.get("error", "API Error"))

    sc = getattr(resp, "status_code", 200)
    if not (200 <= sc < 300):
        raise RuntimeError(f"Backend {sc}: {_read_text(resp)}")

    ctype = (resp.headers.get("Content-Type") or "").lower()
    if "application/json" not in ctype:
        raise RuntimeError(
            f"Backend did not return JSON (Content-Type: {ctype}). Body: {_read_text(resp)}"
        )

    data = resp.json()
    values = data.get("data") if isinstance(data, dict) else data

    if not isinstance(values, list):
        preview = json.dumps(data, default=str)[:400]
        raise RuntimeError(f"Unexpected JSON for tag values. Preview: {preview}")

    tag_meta = {}
    if isinstance(data, dict) and isinstance(data.get("tag"), dict):
        tag_meta = data["tag"]

    return values, tag_meta


def add_value(tag_id, tag_value, description, user):
    headers = {
        "Accept": "text/html,application/json",
        "ApiKey": get_api_key(),
        "X-API-Key": get_api_key()
    }
    payload = {
        "action": "add",
        "add_value": "1",
        "tag_id": tag_id,
        "tag_value": tag_value,
        "description": description,
        "user": user,
    }
    resp = safe_request(api_url("/tag_values"), method="POST", headers=headers, data=payload, verify=False)

    if isinstance(resp, dict) and resp.get("error"):
        raise RuntimeError(resp["error"])

    sc = getattr(resp, "status_code", 0)
    if not (200 <= sc < 400):
        raise RuntimeError(f"Request error: {sc}")


def update_value(tag_entry_id, tag_id, tag_value, description, user):
    headers = {"Accept": "text/html,application/json", "ApiKey": get_api_key(), "X-API-Key": get_api_key()}
    payload = {
        "action": "update",
        "update_value": "1",
        "tag_entry_id": tag_entry_id,
        "tag_id": tag_id,
        "tag_value": tag_value,
        "description": description,
        "user": user,
    }
    resp = safe_request(api_url("/tag_values"), method="POST", headers=headers, data=payload, verify=False)

    if isinstance(resp, dict) and resp.get("error"):
        raise RuntimeError(resp["error"])

    sc = getattr(resp, "status_code", 0)
    if not (200 <= sc < 400):
        raise RuntimeError(f"Update failed ({sc}): {_read_text(resp)}")


def delete_value(tag_entry_id, tag_id, tag_value, user):
    headers = {"Accept": "text/html,application/json", "ApiKey": get_api_key(), "X-API-Key": get_api_key()}
    payload = {"tag_entry_id": tag_entry_id, "tag_id": tag_id, "user": user, "tag_value": tag_value}

    resp = safe_request(api_url("/delete_tag_value"), method="POST", headers=headers, data=payload, verify=False)

    if isinstance(resp, dict) and resp.get("error"):
        raise RuntimeError(resp["error"])

    sc = getattr(resp, "status_code", 0)
    if not (200 <= sc < 400):
        body = _read_text(resp).lower()
        if "integrity" in body or "constraint" in body or "foreign key" in body:
            raise RuntimeError("Cannot delete the tag value as it has associated courses tagged to it")
        raise RuntimeError(f"Delete failed ({sc}): {_read_text(resp)}")


def main():
    try:
        method = os.environ.get("REQUEST_METHOD", "GET").upper()
        user = (
            os.environ.get("REMOTE_USER", "")
            or os.environ.get("HTTP_REMOTE_USER", "")
            or "unknown"
        )
        
        if method == "POST" and not can_write(user):
            tag_id_q = get_qs_param("tag_id").strip() or get_qs_param("selected_tag").strip()
            return redirect_with_messages(
                [("danger", "Read-only account: you can view tag values, but you cannot add/edit/delete.")],
                extra_qs={"tag_id": tag_id_q}
            )

        messages = parse_messages_from_qs()

        tag_id = get_qs_param("tag_id").strip() or get_qs_param("selected_tag").strip()
        edit_mode = get_qs_param("edit").strip() == "1"

        if method == "POST":
            form = cgi.FieldStorage()
            action = (form.getfirst("action") or "").lower()

            tag_id_form = (form.getfirst("tag_id") or form.getfirst("selected_tag") or tag_id).strip()
            keep_qs = {"tag_id": tag_id_form}

            try:
                if action == "add":
                    tag_value = (form.getfirst("tag_value") or "").strip()
                    description = (form.getfirst("description") or "").strip()

                    if not tag_id_form:
                        messages.append(("danger", "Missing tag_id"))
                    elif not tag_value:
                        messages.append(("danger", "Tag value required"))
                    else:
                        try:
                            existing_values, _ = fetch_values_for_tag(tag_id_form)
                            exists = any(
                                (v.get("tag_value") or "").strip().lower() == tag_value.lower()
                                for v in existing_values
                                if isinstance(v, dict)
                            )
                            if exists:
                                messages.append(("danger", f"Tag value '{tag_value}' already exists"))
                                return redirect_with_messages(messages, extra_qs=keep_qs)
                        except Exception:
                            pass

                        try:
                            add_value(tag_id_form, tag_value, description, user)
                            messages.append(("success", f"Tag value '{tag_value}' has been added successfully"))
                        except Exception as e:
                            messages.append(("danger", str(e)))

                elif action == "delete":
                    tag_entry_id = (
                        (form.getfirst("tag_entry_id") or "").strip()
                        or (form.getfirst("value_id") or "").strip()
                    )
                    tag_value = (form.getfirst("tag_value") or "").strip()

                    if not tag_entry_id:
                        messages.append(("danger", "Missing tag_entry_id"))
                    else:
                        try:
                            delete_value(tag_entry_id, tag_id_form, tag_value, user)
                            messages.append(("success", f"Tag value '{tag_value}' deleted"))
                        except Exception as e:
                            messages.append(("danger", str(e)))

                elif action == "update":
                    tag_entry_id = (
                        (form.getfirst("tag_entry_id") or "").strip()
                        or (form.getfirst("value_id") or "").strip()
                    )
                    tag_value = (form.getfirst("tag_value") or "").strip()
                    description = (form.getfirst("description") or "").strip()

                    if not tag_entry_id:
                        messages.append(("danger", "Missing tag_entry_id"))
                    else:
                        update_value(tag_entry_id, tag_id_form, tag_value, description, user)
                        messages.append(("success", f"Tag value '{tag_value}' updated"))

                else:
                    messages.append(("danger", "Unknown action"))

            except Exception as e:
                messages.append(("danger", f"Operation failed: {e}"))

            return redirect_with_messages(messages, extra_qs=keep_qs)

        tags = []
        values = []
        tag_meta = {}

        try:
            tags = fetch_tags_list()
        except Exception as e:
            messages.append(("danger", f"Failed to load tags list: {e}"))

        if tag_id:
            try:
                values, tag_meta = fetch_values_for_tag(tag_id)
            except Exception as e:
                messages.append(("danger", f"Failed to load tag values: {e}"))

        html = env.get_template("tag_values.html").render(
            base_path=BASE_PATH,
            ext=EXT,
            messages=messages,
            user=user,
            tags=tags,
            selected_tag_id=tag_id,
            edit_mode=edit_mode,
            tag=tag_meta,
            values=values,
            page_name="tag_values",
            can_write=can_write(user)
        )

        print_headers(extra={
            "Cache-Control": "no-store, no-cache, must-revalidate, max-age=0",
            "Pragma": "no-cache",
            "Expires": "0"
        })
        sys.stdout.write(html)

    except Exception:
        print_headers()
        esc = (
            traceback.format_exc()
            .replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
        )
        sys.stdout.write(f"<h1>tag_values.py crashed</h1><pre>{esc}</pre>")


if __name__ == "__main__":
    main()
