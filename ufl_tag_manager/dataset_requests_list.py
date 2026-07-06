#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import cgi
import cgitb

from jinja2 import Environment, FileSystemLoader, select_autoescape
from env_config import (
    get_current_user, get_base_path,
    get_user_role, is_in_user_access, is_admin_only_mode,
)
from libs.dataset_request_db import (
    get_admin_requests,
    refresh_existing_request,
    set_nightly_refresh,
    edit_request,
    delete_request,
)

cgitb.enable()

ROOT      = os.path.dirname(os.path.abspath(__file__))
env       = Environment(
    loader=FileSystemLoader(os.path.join(ROOT, "templates")),
    autoescape=select_autoescape(["html", "xml"]),
)
PAGE_SIZE = 25


def render(template_name, **kwargs):
    print("Content-Type: text/html; charset=utf-8\n")
    print(env.get_template(template_name).render(**kwargs))


def main():
    form         = cgi.FieldStorage()
    method       = os.environ.get("REQUEST_METHOD", "GET").upper()
    current_user = get_current_user()

    is_admin = get_user_role(current_user) == "admin"

    if not is_admin:
        render("dataset_requests_list.html",
            current_user=current_user,
            base_path=get_base_path(),
            page_name="dataset_requests_list",
            access_denied=True,
            is_admin=False,
            user_role="read",
            requests=[],
            message="", error="",
            showing=0, total=0,
            total_pages=0, current_page=1,
            endpoint_filter="", table_filter="", header_filter="",
            endpoint_options=[],
            ext=".py",
        )
        return

    message = ""
    error   = ""

    # ── Handle POST actions ──────────────────────────────────────────────────
    if method == "POST":
        action     = form.getfirst("action", "").strip()
        request_id = form.getfirst("request_id", "").strip()

        if not request_id:
            error = "Invalid request — no request ID provided."

        elif action == "row_refresh":
            try:
                refresh_existing_request(int(request_id))
                message = f"Request #{request_id} will be refreshed shortly."
            except ValueError as exc:
                error = str(exc)
            except Exception as exc:
                error = f"Failed to refresh request: {exc}"

        elif action == "set_nightly":
            nightly = form.getfirst("nightly_refresh", "0").strip()
            try:
                set_nightly_refresh(int(request_id), nightly == "1")
                flag_label = "enabled" if nightly == "1" else "disabled"
                message = f"Nightly refresh {flag_label} for request #{request_id}."
            except Exception as exc:
                error = f"Failed to update nightly refresh: {exc}"

        elif action == "edit" and is_admin:
            table_name          = form.getfirst("table_name", "").strip() or None
            dataset_description = form.getfirst("dataset_description", "").strip() or None
            schema_name         = form.getfirst("schema_name", "").strip() or None
            try:
                edit_request(
                    int(request_id),
                    table_name=table_name,
                    dataset_description=dataset_description,
                    schema_name=schema_name,
                )
                message = f"Request #{request_id} updated successfully."
            except ValueError as exc:
                error = str(exc)
            except Exception as exc:
                error = f"Failed to update request: {exc}"

        elif action == "delete" and is_admin:
            try:
                delete_request(int(request_id))
                message = f"Request #{request_id} deleted."
            except ValueError as exc:
                error = str(exc)
            except Exception as exc:
                error = f"Failed to delete request: {exc}"

        else:
            error = "Unknown or unauthorized action."

    # ── Filters ─────────────────────────────────────────────────────────────
    endpoint_filter = form.getfirst("endpoint_filter", "").strip()
    table_filter    = form.getfirst("table_filter",    "").strip()
    header_filter   = form.getfirst("header_filter",   "").strip()

    # ── Pagination ───────────────────────────────────────────────────────────
    try:
        current_page = max(1, int(form.getfirst("page", 1)))
    except (ValueError, TypeError):
        current_page = 1

    # ── Fetch admin datasets ─────────────────────────────────────────────────
    requests, total = get_admin_requests(
        endpoint_filter=endpoint_filter or None,
        table_filter=table_filter    or None,
        header_filter=header_filter   or None,
        page=current_page,
        page_size=PAGE_SIZE,
    )

    total_pages = max(1, (total + PAGE_SIZE - 1) // PAGE_SIZE)

    # Distinct endpoints for filter dropdown
    all_rows, _ = get_admin_requests(page=1, page_size=9999)
    endpoint_options = sorted(set(r["endpoint"] for r in all_rows if r.get("endpoint")))

    render("dataset_requests_list.html",
        current_user=current_user,
        base_path=get_base_path(),
        page_name="dataset_requests_list",
        access_denied=False,
        is_admin=is_admin,
        user_role=get_user_role(current_user),
        requests=requests,
        message=message,
        error=error,
        showing=len(requests),
        total=total,
        total_pages=total_pages,
        current_page=current_page,
        endpoint_filter=endpoint_filter,
        table_filter=table_filter,
        header_filter=header_filter,
        endpoint_options=endpoint_options,
        ext=".py",
    )


if __name__ == "__main__":
    main()