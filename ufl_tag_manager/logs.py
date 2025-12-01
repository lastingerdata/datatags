#!/h/cnswww-test.datatags.lastinger/test.datatags.lastinger.ufl.edu/htdocs/ufl_tag_manager/venv/bin/python3
# -*- coding: utf-8 -*-

import os
import json
import traceback
import urllib.parse
from urllib.parse import quote
from html import escape

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
    start = min(candidates)
    return json.loads(text[start:])

def fetch_reports():
   
    headers = {"Accept": "application/json", "ApiKey": API_KEY}
    resp = safe_request(REPORT_LOGS_URL, headers=headers, verify=False)
    data = parse_json_lenient(resp)

    if isinstance(data, list):
        return [r for r in data if isinstance(r, dict)]

    if isinstance(data, dict):
        if isinstance(data.get("reports"), list):
            return [r for r in data["reports"] if isinstance(r, dict)]
        
        out = []
        for v in data.values():
            if isinstance(v, dict) and ("job_history" in v or "report_name" in v):
                out.append(v)
        if out:
            return out

    return []

def latest_run(job_history):
    if not isinstance(job_history, list) or not job_history:
        return None
    return sorted(
        job_history,
        key=lambda r: str(r.get("start_time") or r.get("end_time") or ""),
        reverse=True,
    )[0]

def make_detail_key(report_name, run):
  
    lf = run.get("log_file")
    if lf:
        return str(lf)
    lu = run.get("log_url")
    if lu:
        return str(lu)
    ts = str(run.get("start_time") or run.get("end_time") or "")
    return f"{report_name}|{ts}"

def compute_details_url(report_name, run):
   
    lu = run.get("log_url")
    if lu and (lu.startswith("http://") or lu.startswith("https://")):
        return lu

    detail_key = make_detail_key(report_name, run)
    return f"{BASE_PATH}/logs{EXT}?detail={quote(detail_key)}"

def build_summary_rows(reports):
    rows = []
    for rep in reports:
        name = rep.get("report_name") or "Unknown"
        desc = rep.get("description") or ""
        last = latest_run(rep.get("job_history") or [])
        if not last:
            continue
        rows.append({
            "report_name": name,
            "description": desc,
            "start_time": last.get("start_time", ""),
            "end_time": last.get("end_time", ""),
            "result": last.get("result_code", last.get("status", "")),
            "detail_key": make_detail_key(name, last),
            "details_url": compute_details_url(name, last),
        })
    rows.sort(key=lambda r: r["report_name"].lower())
    return rows

def build_history_rows(report):
    rows = []
    name = report.get("report_name") or "Unknown"
    desc = report.get("description") or ""
    for run in report.get("job_history") or []:
        rows.append({
            "report_name": name,
            "description": desc,
            "start_time": run.get("start_time", ""),
            "end_time": run.get("end_time", ""),
            "result": run.get("result_code", run.get("status", "")),
            "detail_key": make_detail_key(name, run),
            "details_url": compute_details_url(name, run),
        })
    rows.sort(key=lambda r: str(r["start_time"] or r["end_time"] or ""), reverse=True)
    return rows

def find_run_by_detail_key(reports, detail_key):
    detail_key = str(detail_key)

    for rep in reports:
        for run in rep.get("job_history") or []:
            if str(run.get("log_file") or "") == detail_key:
                return rep, run
            if str(run.get("log_url") or "") == detail_key:
                return rep, run

   
    if "|" in detail_key:
        name, ts = detail_key.split("|", 1)
        for rep in reports:
            rep_name = rep.get("report_name") or "Unknown"
            if rep_name == name:
                for run in rep.get("job_history") or []:
                    if str(run.get("start_time") or "") == ts or str(run.get("end_time") or "") == ts:
                        return rep, run
    return None, None

def fetch_log_detail_from_reports(detail_key):
    reports = fetch_reports()
    rep, run = find_run_by_detail_key(reports, detail_key)
    if not rep or not run:
        raise RuntimeError(f"No matching log run found for key: {detail_key}")

   
    for f in ["log_file_end", "log_output", "log_text"]:
        if run.get(f):
            return f"Report: {rep.get('report_name')}\nField: {f}\n\n{run[f]}"

    
    return json.dumps(
        {"report_name": rep.get("report_name"), "description": rep.get("description"), **run},
        indent=2
    )

def render_detail_page(content, detail_key):
    print("Content-Type: text/html; charset=utf-8")
    print()
    print("<!DOCTYPE html>")
    print("<html><head><meta charset='utf-8'>")
    print("<title>Report Log Details</title>")
    print("<style>")
    print("body{font-family:system-ui,-apple-system,BlinkMacSystemFont,sans-serif;padding:16px;background:#f3f4f6}")
    print("a{text-decoration:none;color:#2563eb}")
    print("pre{background:#0b1020;color:#e5e7eb;padding:16px;border-radius:6px;overflow-x:auto;font-size:13px;line-height:1.5}")
    print("</style></head><body>")
    print(f"<p><a href='{BASE_PATH}/logs{EXT}'>&larr; Back to all reports</a></p>")
    print(f"<p><small>Detail key: {escape(str(detail_key))}</small></p>")
    print("<pre>")
    print(escape(content))
    print("</pre></body></html>")


def main():
    try:
        qs = urllib.parse.parse_qs(os.environ.get("QUERY_STRING", ""))

      
        detail_key = qs.get("detail", [None])[0]
        if detail_key:
            try:
                content = fetch_log_detail_from_reports(detail_key)
                render_detail_page(content, detail_key)
            except Exception:
                print("Content-Type: text/html; charset=utf-8")
                print()
                esc = (
                    traceback.format_exc()
                    .replace("&", "&amp;")
                    .replace("<", "&lt;")
                    .replace(">", "&gt;")
                )
                print("<h1>Failed to load log details</h1>")
                print(f"<p>detail param: {escape(str(detail_key))}</p>")
                print("<pre>")
                print(esc)
                print("</pre>")
            return

      
        messages = []
        try:
            reports = fetch_reports()
        except Exception as e:
            messages.append(("danger", f"Failed to load logs: {e}"))
            reports = []

        report_name_filter = qs.get("report", [None])[0]
        if report_name_filter:
           
            report = None
            for r in reports:
                if (r.get("report_name") or "Unknown") == report_name_filter:
                    report = r
                    break
            if report:
                rows = build_history_rows(report)
            else:
                messages.append(("danger", f"No history found for report '{report_name_filter}'"))
                rows = []
            view = "history"
        else:
           
            rows = build_summary_rows(reports)
            view = "summary"
            report_name_filter = ""

        print("Content-Type: text/html; charset=utf-8")
        print()
        html = env.get_template("logs.html").render(
            base_path=BASE_PATH,
            ext=EXT,
            messages=messages,
            rows=rows,
            view=view,
            report_name=report_name_filter,
        )
        print(html)

    except Exception:
        print("Content-Type: text/html; charset=utf-8")
        print()
        esc = (
            traceback.format_exc()
            .replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
        )
        print(f"<h1>logscrashed</h1><pre>{esc}</pre>")

if __name__ == "__main__":
    main()
