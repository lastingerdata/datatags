#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, sys, cgi, cgitb, traceback
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


def redirect_with_messages(messages):
    import time
    pairs = [("m", f"{c}:{t}") for c, t in messages]
    pairs.append(("_t", str(int(time.time() * 1000))))
    qs = urllib.parse.urlencode(pairs)
    redirect_url = f"{BASE_PATH}/tags{EXT}" + (f"?{qs}" if qs else "")
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


def fetch_tags_json():
    return db_ops.get_non_segmentation_tags()


def add_tag(name, desc, user):
    db_ops.add_tag(name, desc)
    db_ops.log_action(user, "ADD_TAG", f"tag_name={name}")


def delete_tag(tag_id, user):
    ok = db_ops.delete_tag(int(tag_id))
    if not ok:
        raise RuntimeError("Cannot delete tag (likely has associated values)")
    db_ops.log_action(user, "DELETE_TAG", f"tag_id={tag_id}")


def main():
    try:
        method = os.environ.get("REQUEST_METHOD", "GET").upper()
        user = (
            os.environ.get("REMOTE_USER", "")
            or os.environ.get("HTTP_REMOTE_USER", "")
            or "unknown"
        ).strip()

        if method == "POST" and not can_write(user):
            return redirect_with_messages([("danger", "Read-only account: you can view tags, but you cannot add/delete.")])

        if method == "POST":
            form = cgi.FieldStorage()
            action = (form.getfirst("action") or "").lower()
            messages = []

            try:
                if action == "add":
                    name = (form.getfirst("tag_name") or "").strip()
                    desc = (form.getfirst("description") or "").strip()

                    if not name:
                        messages.append(("danger", "Tag name required"))
                    else:
                        try:
                            existing_tags = fetch_tags_json()
                            exists = any(
                                (t.get("tag_name") or "").strip().lower() == name.lower()
                                for t in (existing_tags or [])
                                if isinstance(t, dict)
                            )
                            if exists:
                                messages.append(("danger", f"Tag '{name}' already exists"))
                                return redirect_with_messages(messages)
                        except Exception:
                            pass

                        add_tag(name, desc, user)
                        messages.append(("success", f"Tag '{name}' added"))

                elif action == "delete":
                    tag_id = (form.getfirst("tag_id") or "").strip()
                    tag_name = (form.getfirst("tag_name") or "").strip()

                    if not tag_id:
                        messages.append(("danger", "Missing tag_id for delete"))
                    else:
                        delete_tag(tag_id, user)
                        label = tag_name or f"ID {tag_id}"
                        messages.append(("success", f"Tag {label} deleted"))

                else:
                    messages.append(("danger", "Unknown action"))

            except Exception as e:
                messages.append(("danger", f"Operation failed: {e}"))

            return redirect_with_messages(messages)

        messages = parse_messages_from_qs()

        try:
            tags = fetch_tags_json()
        except Exception as e:
            tags = []
            messages.append(("danger", f"Failed to load tags: {e}"))

        html = env.get_template("tags.html").render(
            base_path=BASE_PATH,
            ext=EXT,
            tags=tags,
            messages=messages,
            user=user,
            page_name="tags",
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
        sys.stdout.write(f"<h1>tags.py crashed</h1><pre>{esc}</pre>")


if __name__ == "__main__":
    main()