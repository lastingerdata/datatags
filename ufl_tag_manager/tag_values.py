#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, sys, cgi, cgitb, traceback, json
import urllib.parse

cgitb.enable()

from jinja2 import Environment, FileSystemLoader, select_autoescape
from env_config import get_base_path, can_write
import libs.db_ops as db_ops

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


def redirect_with_messages(messages, tag_id=None):
    import time
    pairs = [("m", f"{c}:{t}") for c, t in messages]
    if tag_id not in (None, "", "None"):
        pairs.append(("tag_id", str(tag_id)))
    pairs.append(("_t", str(int(time.time() * 1000))))
    qs = urllib.parse.urlencode(pairs, doseq=True)

    redirect_url = f"{BASE_PATH}/tag_values{EXT}" + (f"?{qs}" if qs else "")
    extra = {
        "Cache-Control": "no-store, no-cache, must-revalidate, max-age=0",
        "Pragma": "no-cache",
        "Location": redirect_url
    }
    print_headers(status="303 See Other", extra=extra)
    print(f'<!DOCTYPE html><html><head><meta http-equiv="refresh" content="0;url={redirect_url}"></head><body>Redirecting...</body></html>')
    sys.exit(0)


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


def get_qs():
    return urllib.parse.parse_qs(os.environ.get("QUERY_STRING", ""), keep_blank_values=True)


def _get_selected_tag_id(tags):
    qs = get_qs()
    raw = (qs.get("tag_id", [""])[0] or "").strip()
    if raw.isdigit():
        return int(raw)
    if tags:
        t0 = tags[0]
        if isinstance(t0, dict) and t0.get("tag_id") is not None:
            try:
                return int(t0["tag_id"])
            except Exception:
                return None
    return None


def main():
    try:
        method = os.environ.get("REQUEST_METHOD", "GET").upper()
        user = (
            os.environ.get("REMOTE_USER", "")
            or os.environ.get("HTTP_REMOTE_USER", "")
            or "unknown"
        ).strip()

        if method == "POST" and not can_write(user):
            return redirect_with_messages([("danger", "Read-only account: you can view tag values, but you cannot add/update/delete.")])

        tags = []
        try:
            tags = db_ops.get_non_segmentation_tags() or []
        except Exception:
            tags = []

        selected_tag_id = _get_selected_tag_id(tags)

        # JSON mode (for dropdown/table ajax if you use it)
        qs = get_qs()
        if method == "GET" and (qs.get("format", [""])[0] or "").strip().lower() == "json":
            if not selected_tag_id:
                print_headers(content_type="application/json; charset=utf-8")
                sys.stdout.write(json.dumps([]))
                return
            values = db_ops.get_tag_values(selected_tag_id) or []
            print_headers(content_type="application/json; charset=utf-8")
            sys.stdout.write(json.dumps(values))
            return

        if method == "POST":
            form = cgi.FieldStorage()
            action = (form.getfirst("action") or "").strip().lower()
            messages = []

            try:
                tag_id = (form.getfirst("tag_id") or "").strip()
                if tag_id.isdigit():
                    tag_id = int(tag_id)
                else:
                    tag_id = selected_tag_id

                if action == "add":
                    tag_value = (form.getfirst("tag_value") or "").strip()
                    desc = (form.getfirst("description") or "").strip()

                    if not tag_id:
                        messages.append(("danger", "Please select a tag first"))
                    elif not tag_value:
                        messages.append(("danger", "Tag value required"))
                    else:
                        existing = db_ops.get_tag_values(tag_id) or []
                        exists = any(
                            (v.get("tag_value") or "").strip().lower() == tag_value.lower()
                            for v in existing
                            if isinstance(v, dict)
                        )
                        if exists:
                            messages.append(("danger", f"Tag value '{tag_value}' already exists"))
                        else:
                            db_ops.add_tag_value(tag_id, tag_value, desc)
                            db_ops.log_action(user, "ADD_TAG_VALUE", f"tag_id={tag_id}, tag_value={tag_value}")
                            messages.append(("success", f"Tag value '{tag_value}' added"))

                elif action == "delete":
                    tag_entry_id = (form.getfirst("tag_entry_id") or "").strip()
                    if not tag_entry_id.isdigit():
                        messages.append(("danger", "Missing tag_entry_id for delete"))
                    else:
                        ok = db_ops.delete_tag_value(int(tag_entry_id))
                        if not ok:
                            messages.append(("danger", "Cannot delete tag value (likely has associated values)"))
                        else:
                            db_ops.log_action(user, "DELETE_TAG_VALUE", f"tag_entry_id={tag_entry_id}")
                            messages.append(("success", "Tag value deleted"))

                elif action == "update":
                    tag_entry_id = (form.getfirst("tag_entry_id") or "").strip()
                    updated_value = (form.getfirst("updated_value") or "").strip()
                    updated_description = (form.getfirst("updated_description") or "").strip()

                    if not tag_entry_id.isdigit():
                        messages.append(("danger", "Missing tag_entry_id for update"))
                    elif not updated_value:
                        messages.append(("danger", "Updated value required"))
                    else:
                        ok = db_ops.update_tag_value(int(tag_entry_id), updated_value, updated_description)
                        if not ok:
                            messages.append(("danger", "Update failed"))
                        else:
                            db_ops.log_action(
                                user,
                                "UPDATE_TAG_VALUE",
                                f"tag_entry_id={tag_entry_id}, tag_value={updated_value}"
                            )
                            messages.append(("success", "Tag value updated"))

                else:
                    messages.append(("danger", "Unknown action"))

            except Exception as e:
                messages.append(("danger", f"Operation failed: {e}"))

            return redirect_with_messages(messages, tag_id=tag_id if 'tag_id' in locals() else selected_tag_id)

        messages = parse_messages_from_qs()

        values = []
        if selected_tag_id:
            try:
                values = db_ops.get_tag_values(selected_tag_id) or []
            except Exception as e:
                values = []
                messages.append(("danger", f"Failed to load tag values: {e}"))
        else:
            messages.append(("warning", "No tags available"))

        html = env.get_template("tag_values.html").render(
            base_path=BASE_PATH,
            ext=EXT,
            tags=tags,
            selected_tag_id=selected_tag_id,
            values=values,
            messages=messages,
            user=user,
            page_name="tag_values",
            can_write=can_write(user),
        )

        print_headers(extra={
            "Cache-Control": "no-store, no-cache, must-revalidate, max-age=0",
            "Pragma": "no-cache",
            "Expires": "0"
        })
        sys.stdout.write(html)

    except Exception:
        try:
            print_headers()
        except Exception:
            pass
        esc = (
            traceback.format_exc()
            .replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
        )
        sys.stdout.write(f"<h1>tag_values.py crashed</h1><pre>{esc}</pre>")


if __name__ == "__main__":
    main()