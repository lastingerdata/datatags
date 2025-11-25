#!/usr/bin/env python3

import os
import sys
import cgi
import cgitb
import traceback
import urllib.parse

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


def redirect_with_messages(messages):
    qs = urllib.parse.urlencode([("m", f"{c}:{t}") for c, t in messages])
    extra = {
        "Cache-Control": "no-store",
        "Location": f"{BASE_PATH}/tags{EXT}" + (f"?{qs}" if qs else "")
    }
    print_headers(status="303 See Other", extra=extra)


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


def _read_text(resp, limit=500):
    try:
        return (getattr(resp, "text", "") or "")[:limit]
    except Exception:
        return ""


def fetch_tags_json():
    """
    Mirrors Flask /tags?format=json:
      returns list or {"data": list}
    """
    headers = {
        "Accept": "application/json",
        "ApiKey": get_api_key()
    }

    resp = safe_request(api_url("/tags?format=json"), headers=headers, verify=False)

    if isinstance(resp, dict):
        raise RuntimeError(resp.get("error", "API Error"))

    status = getattr(resp, "status_code", None)
    ctype = (resp.headers.get("Content-Type") or "").lower()

    if status and not (200 <= status < 300):
        body = _read_text(resp)
        raise RuntimeError(f"Backend {status}: {body}")

    if "application/json" not in ctype:
        body = _read_text(resp)
        raise RuntimeError(
            f"Backend did not return JSON (Content-Type: {ctype}). Body: {body}"
        )

    data = resp.json()
    if isinstance(data, dict) and "data" in data:
        data = data["data"]

    if not isinstance(data, list):
        raise RuntimeError("Unexpected JSON structure for tags")

    return data


def add_tag(name, desc, user):
   
    headers = {
        "Accept": "application/json",
        "ApiKey": get_api_key()
    }

    payload = {
        "tag_name": name,
        "description": desc,
        "user": user
    }

    resp = safe_request(
        api_url("/tags"),
        method="POST",
        headers=headers,
        data=payload,
        verify=False
    )

    if isinstance(resp, dict) and resp.get("error"):
        raise RuntimeError(resp["error"])

    sc = getattr(resp, "status_code", 200)
    if not (200 <= sc < 400):
        raise RuntimeError(f"Add failed ({sc}): {_read_text(resp)}")


def delete_tag(tag_id, user):
    
    headers = {"Accept": "text/html,application/json", "ApiKey": get_api_key(), "X-API-Key": get_api_key()}

    payload = {
        "tag_id": tag_id, "user": user
    }

    resp = safe_request(
        api_url("/delete_tag"),
        method="POST",
        headers=headers,
        data=payload,
        verify=False
    )

    if isinstance(resp, dict) and resp.get("error"):
        raise RuntimeError(resp["error"])

    sc = getattr(resp, "status_code", 0)
    if not (200 <= sc < 400):
        raise RuntimeError(f"Delete HTTP failed ({sc}): {_read_text(resp)}")

    final_url = getattr(resp, "url", "") or ""
    location = resp.headers.get("Location", "") or ""
    body = _read_text(resp)

    marker = f"{api_url('/tags')}"
    combined = " ".join([final_url, location, body])

   
    if "deleted=0" in combined or "Cannot delete tag (likely has associated values)" in combined:
        raise RuntimeError("Cannot delete tag (likely has associated values)")
    


def main():
    try:
        method = os.environ.get("REQUEST_METHOD", "GET").upper()
        user = (
            os.environ.get("REMOTE_USER", "")
            or os.environ.get("HTTP_REMOTE_USER", "")
            or "unknown"
        )

        if method == "POST":
            form = cgi.FieldStorage()
            action = (form.getfirst("action") or "").lower()
            messages = []

            try:
                if action == "add":
                    name = (form.getfirst("tag_name") or "").strip()
                    desc = (form.getfirst("description") or "").strip()

                    if not name:
                        messages.append(("danger", "Tag name required"))
                    else:
                        add_tag(name, desc, user)
                        messages.append(("success", f"Tag '{name}' added"))

                elif action == "delete":
                    tag_id = (form.getfirst("tag_id") or "").strip()
                    tag_name = (form.getfirst("tag_name") or "").strip()

                    if not tag_id:
                        messages.append(("danger", "Missing tag_id for delete"))
                    else:
                        delete_tag(tag_id, user)
                        label = tag_name or f"ID {tag_id}"
                        messages.append(("success", f"Tag {label} deleted"))

                else:
                    messages.append(("danger", "Unknown action"))

            except Exception as e:
                messages.append(("danger", f"Operation failed: {e}"))

            return redirect_with_messages(messages)

      
        messages = parse_messages_from_qs()

        try:
            tags = fetch_tags_json()
        except Exception as e:
            tags = []
            messages.append(("danger", f"Failed to load tags: {e}"))

        html = env.get_template("tags.html").render(
            base_path=BASE_PATH,
            ext=EXT,
            tags=tags,
            messages=messages,
            user=user
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
        sys.stdout.write(f"<h1>tags.py crashed</h1><pre>{esc}</pre>")

if __name__ == "__main__":
    main()
    
# #!/usr/bin/env python3.9
# import cgi
# import cgitb; cgitb.enable()
# import requests
# import os
# import html
# from env_config import api_url, api_base, get_api_key, safe_request

# print("Content-Type: text/html\n")

# method = os.environ.get('REQUEST_METHOD', 'GET').upper()
# API_KEY = get_api_key()
# PDF_URL = "/ufl_tag_manager/assets/Tagging%20website%20Documentation.pdf"

# try:
#     headers={"ApiKey": API_KEY}
#     if method == 'POST':
#         form = cgi.FieldStorage()
#         post_data = {key:form.getvalue(key) for key in form.keys()}
#         post_data["ApiKey"] = API_KEY
#         post_data["user"] = os.environ.get("REMOTE_USER", "unknown")
#         r = requests.post(api_url("/tags"), headers=headers, data=post_data, verify=False)
#     else:
#         query_string = os.environ.get("QUERY_STRING", "")
#         url = api_url("/tags") + ("?" + query_string if query_string else "")
#         r = safe_request(url, headers=headers, verify=False)

#     if isinstance(r, dict) :
#         print(f"<h1>{r['error']}</h1>")
#     else:
#         html_out = r.text
#         html = r.text
#         html = html.replace('href="/tags_index"', 'href="/ufl_tag_manager/home"')
#         html = html.replace('action="/delete_tag"', 'action="/ufl_tag_manager/delete_tag"')
#         html = html.replace('action="/tags"', 'action="/ufl_tag_manager/tags"')
#         html = html.replace('/static/docs/Tagging%20website%20Documentation.pdf', PDF_URL)\
#                     .replace('href="#"', f'href="{PDF_URL}" target="_blank" rel="noopener"')\
#                     .replace('>About</a>', f' target="_blank" rel="noopener" href="{PDF_URL}">About</a>')
#         print(html)

# except Exception as e:
#     print(f"<h1>Error: {e}</h1>")
