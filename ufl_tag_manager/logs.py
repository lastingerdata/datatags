#!/h/cnswww-test.datatags.lastinger/test.datatags.lastinger.ufl.edu/htdocs/ufl_tag_manager/venv/bin/python3
# -*- coding: utf-8 -*-

import os
import json
import traceback
import urllib.parse
from html import escape
from urllib.parse import quote, quote_plus

from jinja2 import Environment, FileSystemLoader, select_autoescape
from env_config import safe_request

BASE_PATH = "/ufl_tag_manager"
EXT = ".py"

REPORT_LOGS_URL = "https://compute.lastinger.center.ufl.edu/report_logs"
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
        raise RuntimeError(f"Logs endpoint did not return JSON. Snippet: {snippet}")

    return json.loads(text[min(candidates):])

def fetch_reports():
    headers = {"Accept": "application/json", "ApiKey": API_KEY}
    resp = safe_request(REPORT_LOGS_URL, headers=headers, verify=False)
    data = parse_json_lenient(resp)

    if isinstance(data, list):
        return [r for r in data if isinstance(r, dict)]

    if isinstance(data, dict):
        if isinstance(data.get("reports"), list):
            return data["reports"]

        return [
            v for v in data.values()
            if isinstance(v, dict) and ("job_history" in v or "report_name" in v)
        ]

    return []

def latest_run(job_history):
    if not job_history:
        return None
    return sorted(
        job_history,
        key=lambda r: str(r.get("start_time") or r.get("end_time") or ""),
        reverse=True,
    )[0]

def make_detail_key(report_name, run):
    if run.get("log_file"):
        return str(run["log_file"])
    if run.get("log_url"):
        return str(run["log_url"])
    ts = str(run.get("start_time") or run.get("end_time") or "")
    return f"{report_name}|{ts}"

def compute_details_url(report_name, run):
    if run.get("log_url", "").startswith("http"):
        return run["log_url"]

    return f"{BASE_PATH}/logs{EXT}?detail={quote(make_detail_key(report_name, run))}"

def build_summary_rows(reports):
    rows = []
    for r in reports:
        last = latest_run(r.get("job_history") or [])
        if not last:
            continue
        rows.append({
            "report_name": r.get("report_name", "Unknown"),
            "description": r.get("description", ""),
            "start_time": last.get("start_time", ""),
            "end_time": last.get("end_time", ""),
            "result": last.get("result_code", last.get("status", "")),
            "details_url": compute_details_url(r.get("report_name"), last),
        })
    return sorted(rows, key=lambda x: x["report_name"].lower())


def build_history_rows(report):
    rows = []
    for run in report.get("job_history") or []:
        rows.append({
            "report_name": report.get("report_name", "Unknown"),
            "description": report.get("description", ""),
            "start_time": run.get("start_time", ""),
            "end_time": run.get("end_time", ""),
            "result": run.get("result_code", run.get("status", "")),
            "details_url": compute_details_url(report.get("report_name"), run),
        })
    return sorted(rows, key=lambda r: r["start_time"], reverse=True)


def find_run_by_key(reports, key):
    for r in reports:
        for run in r.get("job_history") or []:
            if key in (str(run.get("log_file")), str(run.get("log_url"))):
                return r, run
    return None, None


def fetch_log_detail(key):
    reports = fetch_reports()
    rep, run = find_run_by_key(reports, key)
    if not rep or not run:
        raise RuntimeError("Log not found")

    for f in ["log_file_end", "log_output", "log_text"]:
        if run.get(f):
            return run[f]

    return json.dumps(run, indent=2)


def main():
    try:
        qs = urllib.parse.parse_qs(os.environ.get("QUERY_STRING", ""))

        detail = qs.get("detail", [None])[0]
        if detail:
            content = fetch_log_detail(detail)
            print("Content-Type: text/html; charset=utf-8\n")
            print(env.get_template("logs.html").render(
                base_path=BASE_PATH,
                ext=EXT,
                view="detail",
                detail_key=detail,
                content=content,
                rows=[],
                messages=[]
            ))
            return

        reports = fetch_reports()
        report_filter = qs.get("report", [None])[0]

        if report_filter:
            report = next((r for r in reports if r.get("report_name") == report_filter), None)
            rows = build_history_rows(report) if report else []
            view = "history"
        else:
            rows = build_summary_rows(reports)
            view = "summary"

        print("Content-Type: text/html; charset=utf-8\n")
        print(env.get_template("logs.html").render(
            base_path=BASE_PATH,
            ext=EXT,
            view=view,
            report_name=report_filter or "",
            rows=rows,
            messages=[]
        ))

    except Exception:
        print("Content-Type: text/html; charset=utf-8\n")
        print("<h1>Logs crashed</h1>")
        print("<pre>")
        print(escape(traceback.format_exc()))
        print("</pre>")


if __name__ == "__main__":
    main()
