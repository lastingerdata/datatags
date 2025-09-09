#!/usr/bin/env python3.9
import os
import cgi
import cgitb
import requests
from env_config import get_api_key

cgitb.enable()

API_URL = "https://sushma.lastinger.center.ufl.edu/delete_tag_value"
API_KEY = get_api_key()

method = os.environ.get("REQUEST_METHOD", "GET").upper()

if method == "POST":
    form = cgi.FieldStorage()
    tag_entry_id = form.getvalue("tag_entry_id")
    tag_id = form.getvalue("tag_id")

    if tag_entry_id:
        try:
            headers = {"ApiKey": API_KEY}
            post_data = {
                "tag_entry_id": tag_entry_id,
                "tag_id": tag_id,
                "user": os.environ.get("REMOTE_USER", "unknown")
            }

            r = requests.post(API_URL, headers=headers, data=post_data, verify=False, allow_redirects=False)
            redirect_url = r.headers.get('Location', '/tag_values')
            redirect_url = redirect_url.replace('/tag_values', '/ufl_tag_manager/tag_values')
            print("Status: 303 See Other")
            print(f"Location: {redirect_url}\n")

        except Exception as e:
            print("Content-Type: text/html\n")
            print(f"<h1 style='color:red;'>Error deleting tag value: {e}</h1>")
    else:
        print("Content-Type: text/html\n")
        print("<h1 style='color:red;'>Missing tag_entry_id</h1>")
else:
    print("Content-Type: text/html\n")
    print("<h1>Invalid request method</h1>")
