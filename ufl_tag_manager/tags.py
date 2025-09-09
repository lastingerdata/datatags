#!/usr/bin/env python3.9
import cgi
import cgitb; cgitb.enable()
import requests
import os
import html
from env_config import api_url, api_base, get_api_key, safe_request

print("Content-Type: text/html\n")

method = os.environ.get('REQUEST_METHOD', 'GET').upper()
API_KEY = get_api_key()
PDF_URL = "/ufl_tag_manager/assets/Tagging%20website%20Documentation.pdf"

try:
    headers={"ApiKey": API_KEY}
    if method == 'POST':
        form = cgi.FieldStorage()
        post_data = {key:form.getvalue(key) for key in form.keys()}
        post_data["ApiKey"] = API_KEY
        post_data["user"] = os.environ.get("REMOTE_USER", "unknown")
        r = requests.post(api_url("/tags"), headers=headers, data=post_data, verify=False)
    else:
        query_string = os.environ.get("QUERY_STRING", "")
        url = api_url("/tags") + ("?" + query_string if query_string else "")
        r = safe_request(url, headers=headers, verify=False)

    if isinstance(r, dict) :
        print(f"<h1>{r['error']}</h1>")
    else:
        html_out = r.text

        html = r.text
        html = html.replace('href="/"', 'href="/ufl_tag_manager/home"')
        html = html.replace('action="/delete_tag"', 'action="/ufl_tag_manager/delete_tag"')
        html = html.replace('action="/tags"', 'action="/ufl_tag_manager/tags"')
        html = html.replace('/static/docs/Tagging%20website%20Documentation.pdf', PDF_URL)\
                .replace('href="#"', f'href="{PDF_URL}" target="_blank" rel="noopener"')\
                .replace('>About</a>', f' target="_blank" rel="noopener" href="{PDF_URL}">About</a>')
        print(html)

except Exception as e:
    print(f"<h1>Error: {e}</h1>")
