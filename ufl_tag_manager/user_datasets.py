#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import cgi
import cgitb

from jinja2 import Environment, FileSystemLoader, select_autoescape
from env_config import get_current_user, get_base_path, get_user_role, is_in_user_access
from libs.dataset_request_db import get_user_requests, refresh_existing_request

cgitb.enable()

ROOT      = os.path.dirname(os.path.abspath(__file__))
env       = Environment(
    loader=FileSystemLoader(os.path.join(ROOT, "templates")),
    autoescape=select_autoescape(["html", "xml"]),
)
PAGE_SIZE = 25

def render(template, **kw):
    print("Content-Type: text/html; charset=utf-8\n")
    print(env.get_template(template).render(**kw))


def _denied(current_user, is_admin, user_role):
    render("user_datasets.html",
        current_user=current_user,
        base_path=get_base_path(),
        page_name="user_datasets",
        access_denied=True,
        is_admin=is_admin, user_role=user_role,
        requests=[], message="", error="",
        showing=0, total=0, total_pages=0, current_page=1,
        ext=".py",
    )

def main():
    form         = cgi.FieldStorage()
    method       = os.environ.get("REQUEST_METHOD", "GET").upper()
    current_user = get_current_user()
    user_role    = get_user_role(current_user)
    is_admin     = user_role == "admin"

    if not is_in_user_access(current_user):
        _denied(current_user, is_admin, user_role)
        return

    message = error = ""

    if method == "POST":
        action     = form.getfirst("action", "").strip()
        request_id = form.getfirst("request_id", "").strip()

        if not request_id:
            error = "Invalid request — no request ID provided."
        elif action == "row_refresh":
            try:
                refresh_existing_request(int(request_id))
                message = f"Request #{request_id} will be refreshed shortly."
            except (ValueError, Exception) as exc:
                error = str(exc)
        else:
            error = "Unknown action."

    try:
        current_page = max(1, int(form.getfirst("page", 1)))
    except (ValueError, TypeError):
        current_page = 1

    requests, total = get_user_requests(
        current_user=current_user,
        is_admin=is_admin,
        page=current_page,
        page_size=PAGE_SIZE,
    )
    total_pages = max(1, (total + PAGE_SIZE - 1) // PAGE_SIZE)

    render("user_datasets.html",
        current_user=current_user,
        base_path=get_base_path(),
        page_name="user_datasets",
        access_denied=False,
        is_admin=is_admin,
        user_role=user_role,
        requests=requests,
        message=message, error=error,
        showing=len(requests), total=total,
        total_pages=total_pages, current_page=current_page,
        ext=".py",
    )

if __name__ == "__main__":
    main()