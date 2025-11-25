#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import cgi
import cgitb
import traceback
import urllib.parse
import json

cgitb.enable()

from jinja2 import Environment, FileSystemLoader, select_autoescape
from env_config import api_url, get_api_key, safe_request

ROOT = os.path.dirname(os.path.abspath(__file__))
TEMPLATES = os.path.join(ROOT, "templates")
env = Environment(
    loader=FileSystemLoader(TEMPLATES),
    autoescape=select_autoescape(["html", "xml"])
)

BASE_PATH = "/cgi-bin/ufl_tag_manager"
EXT = ".py"


def print_headers(content_type="text/html; charset=utf-8", status=None, extra=None):
    if status:
        print(f"Status: {status}")
    print(f"Content-Type: {content_type}")
    if extra:
        for k, v in extra.items():
            print(f"{k}: {v}")
    print()


def redirect_with_messages(messages, extra_qs=None):
    pairs = [("m", f"{c}:{t}") for c, t in messages]
    if extra_qs:
        for k, v in extra_qs.items():
            if v is not None and v != "":
                pairs.append((k, str(v)))
    qs = urllib.parse.urlencode(pairs)
    print_headers(
        status="303 See Other",
        extra={
            "Cache-Control": "no-store",
            "Location": f"{BASE_PATH}/tag_values{EXT}" + (f"?{qs}" if qs else "")
        }
    )


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


def get_qs_param(name, default=""):
    qd = urllib.parse.parse_qs(os.environ.get("QUERY_STRING", ""), keep_blank_values=True)
    return (qd.get(name, [default])[0] or default)


def _read_text(resp, limit=600):
    try:
        return (getattr(resp, "text", "") or "")[:limit]
    except Exception:
        return ""


def fetch_tags_list():
    headers = {"Accept": "application/json", "ApiKey": get_api_key()}
    resp = safe_request(api_url("/tags?format=json"), headers=headers, verify=False)

    if isinstance(resp, dict):
        raise RuntimeError(resp.get("error", "API Error"))

    sc = getattr(resp, "status_code", 200)
    if not (200 <= sc < 300):
        raise RuntimeError(f"Backend {sc}: {_read_text(resp)}")

    ctype = (resp.headers.get("Content-Type") or "").lower()
    if "application/json" not in ctype:
        raise RuntimeError(
            f"Backend did not return JSON (Content-Type: {ctype}). Body: {_read_text(resp)}"
        )

    data = resp.json()
    tags = data.get("data") if isinstance(data, dict) else data
    if not isinstance(tags, list):
        preview = json.dumps(data, default=str)[:400]
        raise RuntimeError(f"Unexpected JSON for tags. Preview: {preview}")
    return tags


def fetch_values_for_tag(tag_id):
    headers = {"Accept": "application/json", "ApiKey": get_api_key()}
    url = api_url(f"/tag_values?tag_id={urllib.parse.quote_plus(str(tag_id))}&format=json")
    resp = safe_request(url, headers=headers, verify=False)

    if isinstance(resp, dict):
        raise RuntimeError(resp.get("error", "API Error"))

    sc = getattr(resp, "status_code", 200)
    if not (200 <= sc < 300):
        raise RuntimeError(f"Backend {sc}: {_read_text(resp)}")

    ctype = (resp.headers.get("Content-Type") or "").lower()
    if "application/json" not in ctype:
        raise RuntimeError(
            f"Backend did not return JSON (Content-Type: {ctype}). Body: {_read_text(resp)}"
        )

    data = resp.json()
    values = data.get("data") if isinstance(data, dict) else data
    if not isinstance(values, list):
        preview = json.dumps(data, default=str)[:400]
        raise RuntimeError(f"Unexpected JSON for tag values. Preview: {preview}")

    # optional tag metadata if your API sends it
    tag_meta = {}
    if isinstance(data, dict) and isinstance(data.get("tag"), dict):
        tag_meta = data["tag"]

    return values, tag_meta


def add_value(tag_id, tag_value, description, user):
    headers = {"Accept": "text/html,application/json", "ApiKey": get_api_key(), "X-API-Key": get_api_key(),}
    payload = {"action": "add", "add_value": "1", "tag_id": tag_id, "tag_value": tag_value, "description": description, "user": user,}
    resp = safe_request(api_url("/tag_values"), method="POST", headers=headers, data=payload, verify=False,)
    if isinstance(resp, dict) and resp.get("error"):
        raise RuntimeError(resp["error"])
    sc = getattr(resp, "status_code", 0)
    if not (200 <= sc < 400):
        raise RuntimeError(f"Add failed ({sc}): {_read_text(resp)}")
    
def update_value(tag_entry_id, tag_id, tag_value, description, user):
    headers = {"Accept": "text/html,application/json", "ApiKey": get_api_key(), "X-API-Key": get_api_key(),}
    payload = {"action": "update","update_value": "1", "tag_entry_id" : tag_entry_id,"tag_id": tag_id, "tag_value": tag_value, "description": description, "user": user,}
    resp = safe_request(api_url("/tag_values"), method="POST", headers=headers, data=payload, verify=False,)
    if isinstance(resp, dict) and resp.get("error"):
        raise RuntimeError(resp["error"])
    sc = getattr(resp, "status_code", 0)
    if not (200 <= sc < 400):
        raise RuntimeError(f"Add failed ({sc}): {_read_text(resp)}")
   
def delete_value(tag_entry_id, tag_id, tag_value, user):
  
    headers = {
        "Accept": "text/html,application/json", "ApiKey": get_api_key(), "X-API-Key": get_api_key(),
    }

    payload = {
        "tag_entry_id": tag_entry_id, "tag_id": tag_id, "user": user, "tag_value": tag_value,
    }

    resp = safe_request(
        api_url("/delete_tag_value"), method="POST", headers=headers, data=payload, verify=False,
    )

    if isinstance(resp, dict) and resp.get("error"):
        raise RuntimeError(resp["error"])

    sc = getattr(resp, "status_code", 0)
    if not (200 <= sc < 400):
        raise RuntimeError(f"Delete failed ({sc}): {_read_text(resp)}")

  

def main():
    try:
        method = os.environ.get("REQUEST_METHOD", "GET").upper()
        user = (
            os.environ.get("REMOTE_USER", "")
            or os.environ.get("HTTP_REMOTE_USER", "")
            or "unknown"
        )

        messages = parse_messages_from_qs()

        tag_id = get_qs_param("tag_id").strip() or get_qs_param("selected_tag").strip()
        edit_mode = get_qs_param("edit").strip() == "1"

        if method == "POST":
            form = cgi.FieldStorage()
            action = (form.getfirst("action") or "").lower()

            
            tag_id_form = (form.getfirst("tag_id") or form.getfirst("selected_tag") or tag_id).strip()
            keep_qs = {"tag_id": tag_id_form}
            if edit_mode or (form.getfirst("edit") == "1"):
                keep_qs["edit"] = "1"

            try:
                if action == "add":
                    tag_value = (form.getfirst("tag_value") or "").strip()
                    description = (form.getfirst("description") or "").strip()

                    if not tag_id_form:
                        messages.append(("danger", "Missing tag_id"))
                    elif not tag_value:
                        messages.append(("danger", "Tag value required"))
                    else:
                        add_value(tag_id_form, tag_value, description, user)
                        messages.append(("success", f"Value '{tag_value}' added"))

                elif action == "delete":
                    tag_entry_id = (
                        (form.getfirst("tag_entry_id") or "").strip()
                        or (form.getfirst("value_id") or "").strip()
                    )
                    tag_value = (form.getfirst("tag_value") or "").strip()
                    if not tag_entry_id:
                        messages.append(("danger", "Missing tag_entry_id"))
                    else:
                        delete_value(tag_entry_id, tag_id_form, tag_value, user)
                        label = tag_entry_id or f"ID {tag_value}"
                        messages.append(("success", f"tag {label} deleted"))
                        # messages.append(("success", f"Value {tag_entry_id} deleted"))

                elif action == "update":
                    tag_entry_id = (
                        (form.getfirst("tag_entry_id") or "").strip()
                        or (form.getfirst("value_id") or "").strip()
                    )
                    tag_value = (form.getfirst("tag_value") or "").strip()
                    description = (form.getfirst("description") or "").strip()
                    if not tag_entry_id:
                        messages.append(("danger", "Missing tag_entry_id"))
                    else:
                        update_value(tag_entry_id, tag_id_form, tag_value, description, user)
                        # label = tag_entry_id or f"ID {tag_value}"
                        messages.append(("success", f"TagValue {tag_value} updated"))

                else:
                    messages.append(("danger", "Unknown action"))

            except Exception as e:
                messages.append(("danger", f"Operation failed: {e}"))

            return redirect_with_messages(messages, extra_qs=keep_qs)

        
        tags = []
        values = []
        tag_meta = {}

        try:
            tags = fetch_tags_list()
        except Exception as e:
            messages.append(("danger", f"Failed to load tags list: {e}"))

        if tag_id:
            try:
                values, tag_meta = fetch_values_for_tag(tag_id)
            except Exception as e:
                messages.append(("danger", f"Failed to load tag values: {e}"))

        html = env.get_template("tag_values.html").render(
            base_path=BASE_PATH,
            ext=EXT,
            messages=messages,
            user=user,
            tags=tags,
            selected_tag_id=tag_id,
            edit_mode=edit_mode,
            tag=tag_meta,
            values=values,
        )

        print_headers()
        sys.stdout.write(html)

    except Exception:
        print_headers()
        esc = (
            traceback.format_exc()
            .replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
        )
        sys.stdout.write(f"<h1>tag_values.py crashed</h1><pre>{esc}</pre>")


if __name__ == "__main__":
    main()
    
    
# #!/usr/bin/env python3
# import os
# import cgi
# import cgitb
# import requests
# from env_config import get_api_key, api_url, api_base, safe_request

# cgitb.enable()

# print("Content-Type: text/html\n")
# API_KEY = get_api_key()

# method = os.environ.get("REQUEST_METHOD", "GET").upper()
# headers = {"ApiKey": API_KEY}
# PDF_URL = "/ufl_tag_manager/assets/Tagging%20website%20Documentation.pdf"

# try:
#     if method == "POST":
#         form = cgi.FieldStorage()
#         post_data = {key: form.getvalue(key) for key in form.keys()}
#         post_data["ApiKey"] = API_KEY
#         post_data["user"] = os.environ.get("REMOTE_USER", "unknown")
#         r = requests.post(api_url("/tag_values"), headers=headers, data=post_data, verify=False)
#     else:

#         query_string = os.environ.get("QUERY_STRING", "")
#         url = api_url("/tag_values") + ("?" + query_string if query_string else "")
#         r = safe_request(url, headers=headers, verify=False)
#     if isinstance(r, dict):
#         print(f"<h1>{r['error']}</h1>")
#     else:
#         html = r.text

#         html = html.replace('href="/tags_index"', 'href="/ufl_tag_manager/home"')
#         html = html.replace('action="/tag_values"', 'action="/ufl_tag_manager/tag_values"')
#         html = html.replace('action="/delete_tag_value"', 'action="/ufl_tag_manager/delete_tag_value"')
#         html = html.replace('/static/docs/Tagging%20website%20Documentation.pdf', PDF_URL)\
#                 .replace('href="#"', f'href="{PDF_URL}" target="_blank" rel="noopener"')\
#                 .replace('>About</a>', f' target="_blank" rel="noopener" href="{PDF_URL}">About</a>')
#         print(html)

# except Exception as e:
#     print(f"<h1 style='color:red;'>Error: {e}</h1>")
