#!/usr/bin/env python3
import os
import cgitb
import requests
from env_config import get_api_key, api_url, safe_request

cgitb.enable()

print("Content-Type: text/html\n")
API_KEY = get_api_key()
headers = {"ApiKey": API_KEY}
PDF_URL = "/ufl_tag_manager/assets/Tagging%20website%20Documentation.pdf"

query_string = os.environ.get("QUERY_STRING", "")
full_url = api_url("/section_tags") + ("?" + query_string if query_string else "")

try:
    r = safe_request(full_url, headers=headers, verify=False)
    if isinstance(r, dict):
        print(f"<h1>{r['error']}</h1>")
    else:
        html = r.text
        html = html.replace('href="/"', 'href="/ufl_tag_manager/home"')
        html = html.replace('action="/section_tags_inserts"', 'action="/ufl_tag_manager/add_section_tags"')
        html = html.replace('action="/delete_section_tag"', 'action="/ufl_tag_manager/delete_section_tag"')
        html = html.replace('action="/delete_selected_section_tags"', 'action="/ufl_tag_manager/delete_selected_section_tags"')
        html = html.replace('/static/docs/Tagging%20website%20Documentation.pdf', PDF_URL)\
                .replace('href="#"', f'href="{PDF_URL}" target="_blank" rel="noopener"')\
                .replace('>About</a>', f' target="_blank" rel="noopener" href="{PDF_URL}">About</a>')
        print(html)

except Exception as e:
    print(f"<h1 style='color:red;'>Error: {e}</h1>")
