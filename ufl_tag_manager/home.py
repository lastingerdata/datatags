#!/usr/bin/env python3.9
import cgi
import cgitb; cgitb.enable()
import requests
import os
import html
from urllib.parse import parse_qs
from env_config import api_url, api_base, get_api_key, safe_request

print("Content-Type: text/html; charset=utf-8")
print("")

API_KEY = get_api_key()
PDF_URL = "/ufl_tag_manager/assets/Tagging%20website%20Documentation.pdf"

query = os.environ.get("QUERY_STRING", "")
params = parse_qs(query)
redirect_status = os.environ.get("REDIRECT_STATUS", "")
request_uri = os.environ.get("REQUEST_URI", "")

try:
    headers = {"ApiKey": API_KEY}
    r = safe_request(api_url("/tags_index"), headers=headers, verify=False)
    html_content = r.text
    html_content = html_content.replace('href="/tags_index"', 'href="/ufl_tag_manager/tags_index"')
    html_content = html_content.replace('/section_tags_inserts"', '/ufl_tag_manager/section_tags_inserts"')
    html_content = html_content.replace('/section_tags"', '/ufl_tag_manager/section_tags"')
    html_content = html_content.replace('/tag_values"', '/ufl_tag_manager/tag_values"')
    html_content = html_content.replace('/tags', '/ufl_tag_manager/tags"')
    html_content = html_content.replace('/static/docs/Tagging%20website%20Documentation.pdf', PDF_URL)\
            .replace('href="#"', f'href="{PDF_URL}" target="_blank" rel="noopener"')\
            .replace('>About</a>', f' target="_blank" rel="noopener" href="{PDF_URL}">About</a>')
    # print("<h3>Currently under development, some features may not function as expected.</h3>")
    print(html_content)
except Exception as e:
    print(f"<h1>Error: {html.escape(str(e))}</h1>")
