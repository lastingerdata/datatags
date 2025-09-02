#!/usr/bin/env python3
import os
import cgi
import cgitb
import requests
import certifi

cgitb.enable()

API_URL = "https://sushma.lastinger.center.ufl.edu/section_tags_inserts"
API_KEY = "your-api-key-here"
headers = {"ApiKey": API_KEY}

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
       
        response = requests.post(API_URL, headers=headers, data=post_data, verify=False)
    else:
        
        query_string = os.environ.get("QUERY_STRING", "")
        url = f"{API_URL}?{query_string}" if query_string else API_URL
        response = requests.get(url, headers=headers, verify=False)

    html = response.text


    html = html.replace('href="/"', 'href="/ufl_tag_manager/home.py"')
    html = html.replace('action="/section_tags_inserts"', 'action="/ufl_tag_manager/add_section_tags.py"')
    html = html.replace('action="/delete_section_tag"', 'action="/ufl_tag_manager/delete_section_tag.py"')
    html = html.replace('action="/delete_selected_section_tags"', 'action="/ufl_tag_manager/delete_selected_section_tags.py"')

    print(html)

except Exception as e:
    print(f"<h1 style='color:red;'>Error: {e}</h1>")