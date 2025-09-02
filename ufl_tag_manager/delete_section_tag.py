#!/usr/bin/env python3
import os
import cgi
import cgitb
import requests
import certifi

cgitb.enable()

API_URL = "https://sushma.lastinger.center.ufl.edu/delete_section_tag"
API_KEY = "your-api-key"
headers = {"ApiKey": API_KEY}

method = os.environ.get("REQUEST_METHOD", "GET").upper()

if method == "POST":
    form = cgi.FieldStorage()

    d2l_id = form.getvalue("d2l_OrgUnitId")
    section_id = form.getvalue("genius_sectionId")
    tag_entry_id = form.getvalue("tag_entry_id")

    if d2l_id and section_id and tag_entry_id:
        try:
            post_data = {
                "d2l_OrgUnitId": d2l_id,
                "genius_sectionId": section_id,
                "tag_entry_id": tag_entry_id,
                "user": os.environ.get("REMOTE_USER", "unknown")
            }
            query_string = os.environ.get("QUERY_STRING", "")
            r = requests.post(API_URL, headers=headers, data=post_data, verify=False)

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
            print(f"<h1 style='color:red;'>Error deleting section tag: {e}</h1>")
    else:
        print("Content-Type: text/html\n")
        print("<h1 style='color:red;'>Missing one or more required fields</h1>")
else:
    print("Content-Type: text/html\n")
    print("<h1>Invalid request method. Please use POST.</h1>")