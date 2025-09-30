#!/usr/bin/env python3
import os
import cgi
import cgitb
import requests
import re
import certifi
from env_config import get_api_key, api_url, safe_request

cgitb.enable()

API_KEY = get_api_key()
headers = {"ApiKey": API_KEY}
PDF_URL = "/ufl_tag_manager/assets/Tagging%20website%20Documentation.pdf"

print("Content-Type: text/html\n")

method = os.environ.get("REQUEST_METHOD", "GET").upper()

try:
    if method == "POST":
        form = cgi.FieldStorage()

        post_data = {}
        for key in form.keys():
            if isinstance(form[key], list):
                post_data[key] = [item.value for item in form[key]]
            else:
                post_data[key] = form.getvalue(key)
        post_data["user"] = os.environ.get("REMOTE_USER", "unknown")
       
        r = requests.post(api_url("/section_tags_inserts"), headers=headers, data=post_data, verify=False)
    else:
        
        query_string = os.environ.get("QUERY_STRING", "")
        url = api_url("/section_tags_inserts") + ("?" + query_string if query_string else "")
        r = safe_request(url, headers=headers, verify=False)
    if isinstance(r, dict):
        print(f"<h1>{r['error']}</h1>")
    
    else:
        html = r.text
        html = html.replace('href="/tags_index"', 'href="/ufl_tag_manager/home"')
        html = html.replace('action="/section_tags_inserts"', 'action="/ufl_tag_manager/add_section_tags"')
        html = html.replace('action="/delete_section_tag"', 'action="/ufl_tag_manager/delete_section_tag"')
        html = re.sub(r'href="/section_tags_inserts(\?.*)?"', r'href="/ufl_tag_manager/section_tags_inserts\1"', html)
        html = html.replace('action="/delete_selected_section_tags"', 'action="/ufl_tag_manager/delete_selected_section_tags"')
        html = html.replace('/static/docs/Tagging%20website%20Documentation.pdf', PDF_URL)\
                .replace('href="#"', f'href="{PDF_URL}" target="_blank" rel="noopener"')\
                .replace('>About</a>', f' target="_blank" rel="noopener" href="{PDF_URL}">About</a>')
        print(html)

except Exception as e:
    print(f"<h1 style='color:red;'>Error: {e}</h1>")

