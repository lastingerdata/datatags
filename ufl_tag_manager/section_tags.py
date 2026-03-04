#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import os, sys, cgi, cgitb, traceback
import urllib.parse

cgitb.enable()

from jinja2 import Environment, FileSystemLoader, select_autoescape
from env_config import get_base_path, can_write
import db_ops

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


def redirect_with_messages(messages, extra_qs=None):
    pairs = [("m", f"{c}:{t}") for c, t in messages]
    if extra_qs:
        for k, v in extra_qs.items():
            if v not in (None, ""):
                pairs.append((k, str(v)))
    qs = urllib.parse.urlencode(pairs)
    print_headers(
        status="303 See Other",
        extra={
            "Cache-Control": "no-store",
            "Location": f"{BASE_PATH}/section_tags{EXT}" + (f"?{qs}" if qs else "")
        }
    )
    sys.exit(0)


def _get_current_filters_from_qs():
    qs = urllib.parse.parse_qs(os.environ.get("QUERY_STRING", ""), keep_blank_values=True)
    return {
        "name": (qs.get("name", [""])[0] or "").strip(),
        "wild_card": (qs.get("wild_card", [""])[0] or "").strip(),
        "d2l_OrgUnitId": (qs.get("d2l_OrgUnitId", [""])[0] or "").strip(),
        "genius_sectionId": (qs.get("genius_sectionId", [""])[0] or "").strip(),
        "tag_name_filter": (qs.get("tag_name_filter", [""])[0] or "").strip(),
        "tag_value_filter": (qs.get("tag_value_filter", [""])[0] or "").strip(),
        "page": (qs.get("page", ["1"])[0] or "1").strip(),
        "sort_col": (qs.get("sort_col", [""])[0] or "").strip(),
        "sort_dir": (qs.get("sort_dir", ["asc"])[0] or "asc").strip(),
    }


def main():
    try:
        form = cgi.FieldStorage()
        method = os.environ.get("REQUEST_METHOD", "GET").upper()
        user = (
            os.environ.get("REMOTE_USER", "")
            or os.environ.get("HTTP_REMOTE_USER", "")
            or "unknown"
        ).strip()

        if method == "POST" and not can_write(user):
            extra_qs = _get_current_filters_from_qs()
            redirect_with_messages(
                [("danger", "Read-only account: you can view section tags, but you cannot remove them.")],
                extra_qs=extra_qs
            )

        if method == "POST":
            single_delete = (form.getfirst("single_delete") or "").strip()
            selected_sections = form.getlist("selected_sections")

            items = []
            if single_delete:
                items.append(single_delete)
            elif selected_sections:
                items.extend(selected_sections)

            removed = 0
            messages = []

            if items:
                for item in items:
                    parts = item.split("_", 2)
                    if len(parts) != 3:
                        continue
                    d2l_id, section_id, tag_entry_id = parts
                    if not tag_entry_id:
                        continue
                    try:
                        if d2l_id in ("None", "", None):
                            d2l_id_db = None
                        else:
                            d2l_id_db = d2l_id

                        db_ops.delete_section_tag(d2l_id_db, section_id, tag_entry_id)
                        db_ops.log_action(
                            user,
                            "DELETE_SECTION_TAG",
                            f"d2l_OrgUnitId={d2l_id_db}, genius_sectionId={section_id}, tag_entry_id={tag_entry_id}"
                        )
                        removed += 1
                    except Exception as e:
                        messages.append(("danger", f"Failed to remove tag: {e}"))

                if removed > 0:
                    messages.insert(0, ("success", "Removed selected tag" if removed == 1 else "Removed selected tags"))
            else:
                messages.append(("warning", "No tags selected"))

            extra_qs = _get_current_filters_from_qs()
            redirect_with_messages(messages, extra_qs=extra_qs)

        qs = urllib.parse.parse_qs(os.environ.get("QUERY_STRING", ""), keep_blank_values=True)
        name = (qs.get("name", [""])[0] or "").strip()
        wild_card = (qs.get("wild_card", [""])[0] or "").strip()
        d2l_OrgUnitId = (qs.get("d2l_OrgUnitId", [""])[0] or "").strip()
        genius_sectionId = (qs.get("genius_sectionId", [""])[0] or "").strip()
        tag_name_filter = (qs.get("tag_name_filter", [""])[0] or "").strip()
        tag_value_filter = (qs.get("tag_value_filter", [""])[0] or "").strip()
        sort_col = (qs.get("sort_col", [""])[0] or "").strip()
        sort_dir = (qs.get("sort_dir", ["asc"])[0] or "asc").strip().lower()
        if sort_dir not in ("asc", "desc"):
            sort_dir = "asc"

        messages = parse_messages_from_qs()

        try:
            mappings = db_ops.get_section_tag_mappings(
                name=name or None,
                d2l_OrgUnitId=d2l_OrgUnitId or None,
                genius_sectionId=genius_sectionId or None,
                tag_name=tag_name_filter or None,
                tag_value=tag_value_filter or None,
                wild_card=wild_card or None,
                sort_col=sort_col or "",
                sort_dir=sort_dir or "asc",
            ) or []

            all_vals = db_ops.get_all_tag_values() or []
            tag_values = all_vals

            unique_tag_names = sorted(
                {
                    (x.get("tag_name") or "").strip()
                    for x in all_vals
                    if isinstance(x, dict) and (x.get("tag_name") or "").strip()
                }
            )

            total_count = len(mappings)
            total_pages = 1
            current_page = 1
            per_page = total_count

        except Exception as e:
            mappings = []
            tag_values = []
            unique_tag_names = []
            total_count = 0
            total_pages = 1
            current_page = 1
            per_page = 0
            messages.append(("danger", f"Failed to load section tags: {e}"))

        html = env.get_template("section_tags.html").render(
            base_path=BASE_PATH,
            ext=EXT,
            messages=messages,
            user=user,
            mappings=mappings,
            tag_values=tag_values,
            unique_tag_names=unique_tag_names,
            total_count=total_count,
            total_pages=total_pages,
            current_page=current_page,
            per_page=per_page,
            name=name,
            page_name="section_tags",
            wild_card=wild_card,
            d2l_OrgUnitId=d2l_OrgUnitId,
            genius_sectionId=genius_sectionId,
            tag_name_filter=tag_name_filter,
            tag_value_filter=tag_value_filter,
            can_write=can_write(user),
            sort_col=sort_col,
            sort_dir=sort_dir,
        )

        print_headers()
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
        print(f"<h1>section_tags.py crashed</h1><pre>{esc}</pre>")


if __name__ == "__main__":
    main()