#!/usr/bin/env python3.9
import os
import cgi
import cgitb
import requests
import certifi

cgitb.enable()

# print("Content-Type: text/plain; charset=utf-8")


API_URL = "https://sushma.lastinger.center.ufl.edu/delete_tag_value"
API_KEY = "your-api-key"

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

            r = requests.post(API_URL, headers=headers, data=post_data, verify=False)

            if r.status_code == 200:
                redirect_url = f"/ufl_tag_manager/tag_values.py?selected_tag={tag_id}&deleted=1"
                print("Status: 303 See Other")
                print(f"Location: {redirect_url}\n")
            else:
                redirect_url = f"/ufl_tag_manager/tag_values.py?selected_tag={tag_id}&deleted=0"
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
