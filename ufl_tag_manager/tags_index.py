#!/usr/bin/env python3
import os, sys, cgitb
from jinja2 import Environment, FileSystemLoader, select_autoescape

cgitb.enable()

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)
TEMPLATES = os.path.join(ROOT, "templates")

from env_config import get_base_path, get_current_user, can_edit_tags

env = Environment(
    loader=FileSystemLoader(TEMPLATES),
    autoescape=select_autoescape(["html", "xml"]),
)

def main():
    user = get_current_user()
    html = env.get_template("tags_index.html").render(
        base_path=get_base_path(),
        ext=".py",
        user=user,
        is_admin=can_edit_tags(user),
    )
    print("Content-Type: text/html; charset=utf-8")
    print()
    print(html)

if __name__ == "__main__":
    main()