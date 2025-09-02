#!/usr/bin/env python3
import os
import cgi
import cgitb
import requests
import certifi

cgitb.enable()

print("Content-Type: text/html\n")

API_URL = "https://sushma.lastinger.center.ufl.edu/tag_values"
API_KEY = "your-api-key-here"

method = os.environ.get("REQUEST_METHOD", "GET").upper()
headers = {"ApiKey": API_KEY}

try:
    if method == "POST":
        form = cgi.FieldStorage()
        post_data = {key: form.getvalue(key) for key in form.keys()}
        post_data["user"] = os.environ.get("REMOTE_USER", "unknown")
    
        response = requests.post(API_URL, headers=headers, data=post_data, verify=False)
    else:
      
        query_string = os.environ.get("QUERY_STRING", "")
        url = API_URL + "?" + query_string if query_string else API_URL
        response = requests.get(url, headers=headers, verify=False)

    html = response.text

    html = html.replace('href="/"', 'href="/ufl_tag_manager/home.py"')
    html = html.replace('action="/tag_values"', 'action="/ufl_tag_manager/tag_values.py"')
    html = html.replace('action="/delete_tag_value"', 'action="/ufl_tag_manager/delete_tag_value.py"')

    print(html)

except Exception as e:
    print(f"<h1 style='color:red;'>Error: {e}</h1>")