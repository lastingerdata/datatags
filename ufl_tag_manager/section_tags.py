#!/usr/bin/env python3
import os
import cgitb
import requests
import certifi

cgitb.enable()

print("Content-Type: text/html\n")

API_URL = "https://sushma.lastinger.center.ufl.edu/section_tags"
API_KEY = "your-api-key"
headers = {"ApiKey": API_KEY}

query_string = os.environ.get("QUERY_STRING", "")
full_url = API_URL + "?" + query_string if query_string else API_URL

try:
    r = requests.get(full_url, headers=headers, verify=False)
    html = r.text

    html = html.replace('href="/"', 'href="/ufl_tag_manager/home.py"')
    html = html.replace('action="/section_tags_inserts"', 'action="/ufl_tag_manager/add_section_tags.py"')
    html = html.replace('action="/delete_section_tag"', 'action="/ufl_tag_manager/delete_section_tag.py"')
    html = html.replace('action="/delete_selected_section_tags"', 'action="/ufl_tag_manager/delete_selected_section_tags.py"')

    print(html)

except Exception as e:
    print(f"<h1 style='color:red;'>Error: {e}</h1>")
