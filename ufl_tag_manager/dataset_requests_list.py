#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import cgi
import cgitb

from jinja2 import Environment, FileSystemLoader, select_autoescape
from env_config import (
    get_current_user, get_base_path,
    get_tag_admin_users, get_valid_users, is_admin_only_mode,
)
from libs.dataset_request_db import (
    get_all_dataset_requests,
    refresh_existing_request,
    set_nightly_refresh,
)

cgitb.enable()

ROOT = os.path.dirname(os.path.abspath(__file__))
env  = Environment(
    loader=FileSystemLoader(os.path.join(ROOT, "templates")),
    autoescape=select_autoescape(["html", "xml"]),
)


def render(template_name, **kwargs):
    print("Content-Type: text/html; charset=utf-8\n")
    print(env.get_template(template_name).render(**kwargs))


def main():
    form         = cgi.FieldStorage()
    method       = os.environ.get("REQUEST_METHOD", "GET").upper()
    current_user = get_current_user()

    admin_only = is_admin_only_mode()
    is_admin   = current_user in get_tag_admin_users()
    is_valid   = current_user in get_valid_users()

    if (admin_only and not is_admin) or (not admin_only and not is_valid):
        render("dataset_requests_list.html",
            current_user=current_user,
            base_path=get_base_path(),
            page_name="dataset_requests_list",
            access_denied=True,
            is_admin=False,
            requests=[],
            message="",
            error="",
            showing=0,
            total=0,
            ext=".py",
        )
        return

    message = ""
    error   = ""

    if method == "POST":
        action     = form.getfirst("action", "").strip()
        request_id = form.getfirst("request_id", "").strip()

        if not request_id:
            error = "Invalid request — no request ID provided."

        elif action == "row_refresh":
            # Reset existing completed/failed row back to pending
            try:
                refresh_existing_request(int(request_id))
                message = f"Request #{request_id}  will be refreshed shortly."
            except ValueError as exc:
                error = str(exc)
            except Exception as exc:
                error = f"Failed to refresh request: {exc}"

        elif action == "set_nightly" and is_admin:
            # Toggle nightly refresh flag — admin only
            nightly = form.getfirst("nightly_refresh", "0").strip()
            try:
                set_nightly_refresh(int(request_id), nightly == "1")
                flag_label = "enabled" if nightly == "1" else "disabled"
                message = f"Nightly refresh {flag_label} for request #{request_id}."
            except Exception as exc:
                error = f"Failed to update nightly refresh: {exc}"

        else:
            error = "Unknown action."

    requests = get_all_dataset_requests()

    render("dataset_requests_list.html",
        current_user=current_user,
        base_path=get_base_path(),
        page_name="dataset_requests_list",
        access_denied=False,
        is_admin=is_admin,
        requests=requests,
        message=message,
        error=error,
        showing=len(requests),
        total=len(requests),
        ext=".py",
    )


if __name__ == "__main__":
    main()