#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, cgitb

from jinja2 import Environment, FileSystemLoader, select_autoescape
from env_config import (
    get_current_user, get_base_path, get_user_role,
    is_in_user_access, is_admin_only_mode,
)

cgitb.enable()

ROOT = os.path.dirname(os.path.abspath(__file__))
env  = Environment(
    loader=FileSystemLoader(os.path.join(ROOT, "templates")),
    autoescape=select_autoescape(["html", "xml"]),
)


def render(template, **kw):
    print("Content-Type: text/html; charset=utf-8\n")
    print(env.get_template(template).render(**kw))


def _denied(current_user, user_role):
    render("documentation.html",
        current_user=current_user,
        base_path=get_base_path(),
        page_name="documentation",
        access_denied=True,
        user_role=user_role,
        is_admin=False,
        ext=".py",
    )


def main():
    current_user = get_current_user()
    user_role    = get_user_role(current_user)
    is_admin     = user_role == "admin"
    is_valid     = is_in_user_access(current_user)

    if (is_admin_only_mode() and not is_admin) or (not is_admin_only_mode() and not is_valid):
        _denied(current_user, user_role)
        return

    render("documentation.html",
        current_user=current_user,
        base_path=get_base_path(),
        ext=".py",
        page_name="documentation",
        access_denied=False,
        user_role=user_role,
        is_admin=is_admin,
    )

if __name__ == "__main__":
    main()
