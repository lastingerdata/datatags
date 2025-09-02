#!/usr/bin/env python3
import os
import cgi
import cgitb
import requests
import certifi

cgitb.enable()

API_URL = "https://sushma.lastinger.center.ufl.edu/delete_selected_section_tags"
API_KEY = "your-api-key"
headers = {"ApiKey": API_KEY}

method = os.environ.get("REQUEST_METHOD", "GET").upper()

if method == "POST":
    form = cgi.FieldStorage()
    selected = form.getlist("selected_sections")  

    if selected:
        try:
            post_data = [item for item in selected]
            payload = [("selected_sections", item) for item in post_data]
            payload.append(("user", os.environ.get("REMOTE_USER", "unknown")))

            query_string = os.environ.get("QUERY_STRING", "")

            r = requests.post(API_URL, headers=headers, data=payload, verify=False)

            if r.status_code == 200:
                url = f"/ufl_tag_manager/section_tags.py?deleted=1&{query_string}" if query_string else "/ufl_tag_manager/section_tags.py?deleted=1"
                print("Status: 303 See Other")
                print(f"Location: {url}\n") 
            else:
                url = f"/ufl_tag_manager/section_tags.py?deleted=0&{query_string}" if query_string else "/ufl_tag_manager/section_tags.py?deleted=0"
                print("Status: 303 See Other")
                print(f"Location: {url}\n")

        except Exception as e:
            print("Content-Type: text/html\n")
            print(f"<h1 style='color:red;'>Error deleting section tags: {e}</h1>")
    else:
        print("Content-Type: text/html\n")
        print("<h1 style='color:red;'>No sections selected for deletion.</h1>")
else:
    print("Content-Type: text/html\n")
    print("<h1>Invalid request method. Please use POST.</h1>")