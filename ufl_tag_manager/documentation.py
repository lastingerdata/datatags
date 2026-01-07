#!/usr/bin/env python3
import os, cgitb
from jinja2 import Environment, FileSystemLoader, select_autoescape

from ufl_tag_manager.env_config import get_base_path

cgitb.enable()

ROOT = os.path.dirname(os.path.abspath(__file__))
TEMPLATES = os.path.join(ROOT, "templates")

env = Environment(
    loader=FileSystemLoader(TEMPLATES),
    autoescape=select_autoescape(["html","xml"]),
)

def main():
    html = env.get_template("documentation.html").render(
    base_path=get_base_path(),
    extra=".py",
    user=os.environ.get("REMOTE_USER", "unknown"),
)
    print("Content-Type: text/html; charset=utf-8")
    print()
    print(html)

if __name__ == "__main__":
    main()