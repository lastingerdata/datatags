#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
import cgitb
import traceback
import urllib.parse
from html import escape
from urllib.parse import quote_plus

cgitb.enable()

from jinja2 import Environment, FileSystemLoader, select_autoescape
from env_config import safe_request, get_base_path

BASE_PATH = get_base_path()
EXT = ".py"

RULES_URL = "https://compute.lastinger.center.ufl.edu/rules"
API_KEY = "596fa395d7a9072c06207b119ec415164487d50a37f904d08542305466a80fce"

ROOT = os.path.dirname(os.path.abspath(__file__))
TEMPLATES = os.path.join(ROOT, "templates")

env = Environment(
    loader=FileSystemLoader(TEMPLATES),
    autoescape=select_autoescape(["html", "xml"])
)
env.filters["urlencode"] = lambda s: quote_plus(str(s))


def parse_json_lenient(resp):
    if isinstance(resp, (dict, list)):
        return resp
    try:
        return resp.json()
    except Exception:
        pass

    text = (getattr(resp, "text", "") or "").lstrip()
    if text.lower().startswith("pretty-print"):
        text = text.split("\n", 1)[1] if "\n" in text else ""

    start_brace = text.find("{")
    start_brack = text.find("[")
    candidates = [i for i in (start_brace, start_brack) if i != -1]
    if not candidates:
        snippet = text[:200].replace("<", "&lt;").replace(">", "&gt;")
        raise RuntimeError(f"Rules endpoint did not return JSON. Snippet: {snippet}")

    return json.loads(text[min(candidates):])

def fetch_rules_raw():
    headers = {"Accept": "application/json", "ApiKey": API_KEY}
    resp = safe_request(RULES_URL, headers=headers, verify=False)
    return parse_json_lenient(resp)

def method_to_text(m):
    if isinstance(m, list):
        return "\n".join(str(x) for x in m)
    if m is None:
        return ""
    return str(m)


def tag_value_to_text(v):
    if isinstance(v, list):
        return ", ".join(str(x) for x in v)
    if v is None:
        return ""
    return str(v)


def normalize_rules(raw):
    out = []

    # unwrap wrappers if any
    if isinstance(raw, dict) and isinstance(raw.get("rules"), list):
        raw = raw["rules"]
    if isinstance(raw, dict) and isinstance(raw.get("data"), list):
        raw = raw["data"]

    if isinstance(raw, dict):
        for k, v in raw.items():
            if isinstance(v, dict):
                row = {"rule_name": str(k)}
                row.update(v)
                out.append(row)
        return out
    
    if isinstance(raw, list):
        for item in raw:
            if not isinstance(item, dict):
                continue
            for rule_name, rule_body in item.items():
                if isinstance(rule_body, dict):
                    row = {"rule_name": str(rule_name)}
                    row.update(rule_body)
                    out.append(row)
        return out

    return out


def build_rows(rules):
    rows = []
    for r in rules:
        if not isinstance(r, dict):
            continue

        rows.append({
            "rule_name": r.get("rule_name", "Unknown"),
            "endpoint": r.get("endpoint", ""),
            "segment": r.get("segment", ""),
            "section_tag": r.get("section_tag", ""),
            "tag_name": r.get("tag_name", ""),
            "tag_value_text": tag_value_to_text(r.get("tag_value")),
            "order": r.get("order", ""),
            "column": r.get("column", ""),
            "description": r.get("description", ""),
            "method_source": method_to_text(r.get("method")),
        })

    def _order(v):
        try:
            return int(v)
        except Exception:
            return 999999

    rows.sort(key=lambda x: (
        (x.get("endpoint") or "").lower(),
        (x.get("section_tag") or "").lower(),
        (x.get("tag_name") or "").lower(),
        _order(x.get("order")),
        (x.get("rule_name") or "").lower(),
    ))
    return rows


def main():
    try:
        qs = urllib.parse.parse_qs(os.environ.get("QUERY_STRING", ""))
        messages = []
        try:
            raw = fetch_rules_raw()
            rules = normalize_rules(raw)
            rows = build_rows(rules)
        except Exception as e:
            messages.append(("danger", f"Failed to load rules: {e}"))
            rows = []

        detail_key = qs.get("detail", [None])[0]
        if detail_key:
            match = next((r for r in rows if str(r.get("rule_name")) == str(detail_key)), None)
            if not match:
                messages.append(("danger", f"No matching rule found for '{detail_key}'"))

            print("Content-Type: text/html; charset=utf-8\n")
            print(env.get_template("rules.html").render(
                base_path=BASE_PATH,
                ext=EXT,
                view="detail",
                messages=messages,
                rows=[],
                r=match,
                page_name='rules',
            ))
            return

        print("Content-Type: text/html; charset=utf-8\n")
        print(env.get_template("rules.html").render(
            base_path=BASE_PATH,
            ext=EXT,
            view="list",
            messages=messages,
            rows=rows,
            r=None,
            page_name='rules',
        ))

    except Exception:
        print("Content-Type: text/html; charset=utf-8\n")
        esc = (
            traceback.format_exc()
            .replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
        )
        print(f"<h1>rulescrashed</h1><pre>{esc}</pre>")


if __name__ == "__main__":
    main()
