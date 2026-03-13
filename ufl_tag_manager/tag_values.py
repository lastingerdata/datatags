#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import cgi
import cgitb
import traceback
import urllib.parse

cgitb.enable()

from jinja2 import Environment, FileSystemLoader, select_autoescape
from env_config import get_base_path, can_write, get_current_user, can_edit_tags
from libs import db_ops

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
    qs = urllib.parse.urlencode(pairs)

    redirect_url = f"{BASE_PATH}/tag_values{EXT}" + (f"?{qs}" if qs else "")
    extra = {
        "Cache-Control": "no-store, no-cache, must-revalidate, max-age=0",
        "Pragma": "no-cache",
        "Location": redirect_url,
    }
    print_headers(status="303 See Other", extra=extra)
    print(
        f'<!DOCTYPE html><html><head><meta http-equiv="refresh" content="0;url={redirect_url}"></head>'
        f"<body>Redirecting...</body></html>"
    )
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


def _safe_int(x):
    try:
        return int(str(x).strip())
    except Exception:
        return None


def main():
    try:
        method = os.environ.get("REQUEST_METHOD", "GET").upper()
        user = get_current_user()
        rw = can_write(user)

        form = cgi.FieldStorage()

        # tag_id can come from GET or POST
        tag_id = form.getfirst("tag_id") if method == "POST" else None
        if tag_id is None:
            qs = urllib.parse.parse_qs(os.environ.get("QUERY_STRING", ""), keep_blank_values=True)
            tag_id = (qs.get("tag_id", [""])[0] or "").strip()

        tag_id_int = _safe_int(tag_id)
        selected_tag_id = str(tag_id_int) if tag_id_int is not None else ""

        # POST actions
        if method == "POST":
            if not can_edit_tags(user):
                redirect_with_messages(
                    [("danger", "Read-only account: you can view tag values, but you can’t add/edit/delete them.")],
                    tag_id=selected_tag_id,
                )

            action = (form.getfirst("action") or "").strip().lower()
            messages = []

            try:
                if action == "add":
                    if tag_id_int is None:
                        messages.append(("danger", "Please select a tag first."))
                    else:
                        tag_value = (form.getfirst("tag_value") or "").strip()
                        description = (form.getfirst("description") or "").strip()

                        if not tag_value:
                            messages.append(("danger", "Tag value is required."))
                        else:
                            db_ops.add_tag_value(tag_id_int, tag_value, description)
                            db_ops.log_action(user, "add_tag_value", f"tag_id={tag_id_int}, value={tag_value}")
                            messages.append(("success", f'Tag value "{tag_value}" added.'))

                elif action == "delete":
                    tag_entry_id = _safe_int(form.getfirst("tag_entry_id"))
                    tag_value = (form.getfirst("tag_value") or "").strip()

                    if tag_entry_id is None:
                        messages.append(("danger", "Missing tag_entry_id for delete."))
                    else:
                        ok = db_ops.delete_tag_value(tag_entry_id)
                        if ok:
                            db_ops.log_action(user, "delete_tag_value", f"tag_entry_id={tag_entry_id}, value={tag_value}")
                            messages.append(("success", f'Tag value "{tag_value or tag_entry_id}" deleted.'))
                        else:
                            messages.append(("danger", "Cannot delete tag value (likely has associated section mappings)."))

                elif action == "update":
                    tag_entry_id = _safe_int(form.getfirst("tag_entry_id"))
                    updated_value = (form.getfirst("updated_value") or "").strip()
                    updated_description = (form.getfirst("updated_description") or "").strip()

                    if tag_entry_id is None:
                        messages.append(("danger", "Missing tag_entry_id for update."))
                    elif not updated_value:
                        messages.append(("danger", "Updated value is required."))
                    else:
                        ok = db_ops.update_tag_value(tag_entry_id, updated_value, updated_description)
                        if ok:
                            db_ops.log_action(
                                user,
                                "update_tag_value",
                                f"tag_entry_id={tag_entry_id}, value={updated_value}",
                            )
                            messages.append(("success", f'Tag value "{updated_value}" updated.'))
                        else:
                            messages.append(("danger", "Update failed (no rows changed)."))

                else:
                    messages.append(("danger", "Unknown action."))

            except Exception as e:
                messages.append(("danger", f"Operation failed: {e}"))

            redirect_with_messages(messages, tag_id=selected_tag_id)

        # GET render
        messages = parse_messages_from_qs()

        try:
            tags = db_ops.get_non_segmentation_tags()
        except Exception as e:
            tags = []
            messages.append(("danger", f"Failed to load tags: {e}"))

        values = []
        if tag_id_int is not None:
            try:
                values = db_ops.get_tag_values(tag_id_int)
            except Exception as e:
                values = []
                messages.append(("danger", f"Failed to load tag values: {e}"))

        html = env.get_template("tag_values.html").render(
            base_path=BASE_PATH,
            ext=EXT,
            tags=tags,
            values=values,
            selected_tag_id=selected_tag_id,
            messages=messages,
            user=user,
            page_name="tag_values",
            can_write=can_edit_tags(user),
        )

        print_headers(extra={
            "Cache-Control": "no-store, no-cache, must-revalidate, max-age=0",
            "Pragma": "no-cache",
            "Expires": "0",
        })
        sys.stdout.write(html)

    except SystemExit:
        raise
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