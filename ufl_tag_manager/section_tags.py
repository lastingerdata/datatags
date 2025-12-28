#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
import cgi
import cgitb
import traceback
import urllib.parse
cgitb.enable()
from jinja2 import Environment, FileSystemLoader, select_autoescape
from env_config import api_url, get_api_key, safe_request, get_base_path
ROOT = os.path.dirname(os.path.abspath(__file__))
TEMPLATES = os.path.join(ROOT, "templates")
env = Environment(
   loader=FileSystemLoader(TEMPLATES),
   autoescape=select_autoescape(["html", "xml"])
)
BASE_PATH = get_base_path()
EXT = ".py"

def print_headers(content_type="text/html; charset=utf-8", status=None, extra=None):
    if status:
        print(f"Status: {status}")
    print(f"Content-Type: {content_type}")
    if extra:
        for k, v in extra.items():
            print(f"{k}: {v}")
    print()  # Must be a blank line

def _read_text(resp, limit=800):
   try:
       return (getattr(resp, "text", "") or "")[:limit]
   except Exception:
       return ""

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

def redirect_with_messages(messages, extra_qs=None):
    pairs = [("m", f"{c}:{t}") for c, t in messages]
    if extra_qs:
        for k, v in extra_qs.items():
            if v not in (None, ""):
                pairs.append((k, str(v)))
    qs = urllib.parse.urlencode(pairs)
    print_headers(
        status="303 See Other",
        extra={
            "Cache-Control": "no-store",
            "Location": f"{BASE_PATH}/section_tags{EXT}" + (f"?{qs}" if qs else "")
        }
    )
    sys.exit(0)

def fetch_section_tags_json(qs_dict):
   qs_pairs = []
   for k, v in qs_dict.items():
       if v not in (None, ""):
           qs_pairs.append((k, v))
   qs_pairs.append(("format", "json"))
   qs = urllib.parse.urlencode(qs_pairs)
   headers = {
       "Accept": "application/json",
       "ApiKey": get_api_key(),
       "X-API-Key": get_api_key(),
   }
   resp = safe_request(
       api_url("/section_tags") + ("?" + qs if qs else ""),
       headers=headers,
       verify=False,
   )
   if isinstance(resp, dict):
       raise RuntimeError(resp.get("error", "API Error"))
   sc = getattr(resp, "status_code", 0)
   if not (200 <= sc < 300):
       raise RuntimeError(f"Backend {sc}: {_read_text(resp)}")
   ctype = (resp.headers.get("Content-Type") or "").lower()
   if "application/json" not in ctype:
       raise RuntimeError(
           f"/section_tags?format=json did not return JSON "
           f"(Content-Type: {ctype}). Body: {_read_text(resp)}"
       )
   data = resp.json()
   if not isinstance(data, dict):
       raise RuntimeError("Unexpected JSON structure from /section_tags?format=json")
   data.setdefault("mappings", [])
   data.setdefault("tag_values", [])
   data.setdefault("unique_tag_names", [])
   data.setdefault("total_count", len(data["mappings"]))
   data.setdefault("total_pages", 1)
   data.setdefault("current_page", 1)
   data.setdefault("per_page", data["total_count"])
   return data

def call_delete_section_tag(d2l_id, section_id, tag_entry_id, user):
   headers = {
       "Accept": "text/html,application/json",
       "ApiKey": get_api_key(),
       "X-API-Key": get_api_key(),
   }
   payload = {
       "d2l_OrgUnitId": d2l_id,
       "genius_sectionId": section_id,
       "tag_entry_id": tag_entry_id,
       "user": user or "unknown",
   }
   resp = safe_request(
       api_url("/delete_section_tag"),
       method="POST",
       headers=headers,
       data=payload,
       verify=False,
   )
   if isinstance(resp, dict) and resp.get("error"):
       raise RuntimeError(resp["error"])
   sc = getattr(resp, "status_code", 0)
   if not (200 <= sc < 400):
       raise RuntimeError(f"Delete failed ({sc}): {_read_text(resp)}")

def redirect_to_self():
    loc = f"{BASE_PATH}/section_tags{EXT}"
    print_headers(
        status="303 See Other",
        extra={
            "Location": loc,
            "Cache-Control": "no-store, no-cache, must-revalidate, max-age=0",
            "Pragma": "no-cache",
            "Expires": "0"
        }
    )
    print(f'<html><head><meta http-equiv="refresh" content="0;url={loc}"></head><body>Redirecting...</body></html>')
    sys.stdout.flush()
    sys.exit(0)

def main():
    try:
        form = cgi.FieldStorage()
        method = os.environ.get('REQUEST_METHOD', 'GET').upper()
        user = (
            os.environ.get("REMOTE_USER", "")
            or os.environ.get("HTTP_REMOTE_USER", "")
            or "unknown"
        )

        if method == 'POST':
            single_delete = (form.getfirst("single_delete") or "").strip()
            selected_sections = form.getlist("selected_sections")
            try:
                items = []
                if single_delete:
                    items.append(single_delete)
                elif selected_sections:
                    items.extend(selected_sections)
                if items:
                    for item in items:
                        parts = item.split("_", 2)
                        if len(parts) != 3:
                            continue
                        d2l_id, section_id, tag_entry_id = parts
                        if not tag_entry_id:
                            continue
                        call_delete_section_tag(d2l_id, section_id, tag_entry_id, user)
            except Exception:
                pass
            redirect_to_self()

        # GET: show list with filters
        qs = urllib.parse.parse_qs(os.environ.get("QUERY_STRING", ""), keep_blank_values=True)
        name = (qs.get("name", [""])[0] or "").strip()
        wild_card = (qs.get("wild_card", [""])[0] or "").strip()
        d2l_OrgUnitId = (qs.get("d2l_OrgUnitId", [""])[0] or "").strip()
        genius_sectionId = (qs.get("genius_sectionId", [""])[0] or "").strip()
        tag_name_filter = (qs.get("tag_name_filter", [""])[0] or "").strip()
        tag_value_filter = (qs.get("tag_value_filter", [""])[0] or "").strip()
        page = int((qs.get("page", ["1"])[0] or "1"))
        messages = parse_messages_from_qs()
        try:
            data = fetch_section_tags_json({
                "name": name,
                "wild_card": wild_card,
                "d2l_OrgUnitId": d2l_OrgUnitId,
                "genius_sectionId": genius_sectionId,
                "tag_name_filter": tag_name_filter,
                "tag_value_filter": tag_value_filter,
                "page": page,
            })
            mappings = data["mappings"]
            tag_values = data["tag_values"]
            unique_tag_names = data["unique_tag_names"]
            total_count = data["total_count"]
            total_pages = data["total_pages"]
            current_page = data["current_page"]
            per_page = data["per_page"]
        except Exception as e:
            mappings = []
            tag_values = []
            unique_tag_names = []
            total_count = 0
            total_pages = 1
            current_page = 1
            per_page = 0
            messages.append(("danger", f"Failed to load section tags: {e}"))
        html = env.get_template("section_tags.html").render(
            base_path=BASE_PATH,
            ext=EXT,
            messages=messages,
            user=user,
            mappings=mappings,
            tag_values=tag_values,
            unique_tag_names=unique_tag_names,
            total_count=total_count,
            total_pages=total_pages,
            current_page=current_page,
            per_page=per_page,
            name=name,
            page_name='section_tags',
            wild_card=wild_card,
            d2l_OrgUnitId=d2l_OrgUnitId,
            genius_sectionId=genius_sectionId,
            tag_name_filter=tag_name_filter,
            tag_value_filter=tag_value_filter,
        )
        print_headers()
        sys.stdout.write(html)
    except Exception:
        try:
            print_headers()
        except Exception:
            pass
        esc = (
            traceback.format_exc()
            .replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
        )
        print(f"<h1>section_tags.py crashed</h1><pre>{esc}</pre>")

if __name__ == "__main__":
    main()
   
   
   
# #!/usr/bin/env python3
# import os
# import cgitb
# import requests
# from env_config import get_api_key, api_url, safe_request

# cgitb.enable()

# print("Content-Type: text/html\n")
# API_KEY = get_api_key()
# headers = {"ApiKey": API_KEY}
# PDF_URL = "/ufl_tag_manager/assets/Tagging%20website%20Documentation.pdf"

# query_string = os.environ.get("QUERY_STRING", "")
# full_url = api_url("/section_tags") + ("?" + query_string if query_string else "")

# try:
#     r = safe_request(full_url, headers=headers, verify=False)
#     if isinstance(r, dict):
#         print(f"<h1>{r['error']}</h1>")
#     else:
#         html = r.text
#         # html = html.replace('href="/"', 'href="/ufl_tag_manager/home"')
#         html = html.replace('/tags_index"', '/ufl_tag_manager/home"')
#         html = html.replace('action="/section_tags_inserts"', 'action="/ufl_tag_manager/add_section_tags"')
#         html = html.replace('action="/delete_section_tag"', 'action="/ufl_tag_manager/delete_section_tag"')
#         html = html.replace('action="/delete_selected_section_tags"', 'action="/ufl_tag_manager/delete_selected_section_tags"')
#         html = html.replace('/static/docs/Tagging%20website%20Documentation.pdf', PDF_URL)\
#                 .replace('href="#"', f'href="{PDF_URL}" target="_blank" rel="noopener"')\
#                 .replace('>About</a>', f' target="_blank" rel="noopener" href="{PDF_URL}">About</a>')
#         print(html)

# except Exception as e:
#     print(f"<h1 style='color:red;'>Error: {e}</h1>")
