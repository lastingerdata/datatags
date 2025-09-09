#!/usr/bin/env python3
import os
import cgi
import cgitb
import requests
from env_config import get_api_key

cgitb.enable()

API_URL = "https://sushma.lastinger.center.ufl.edu/delete_tag"

API_KEY = get_api_key()

method = os.environ.get("REQUEST_METHOD", "GET").upper()

try:
    if method == "POST":
        form = cgi.FieldStorage()
        post_data = {key: form.getvalue(key) for key in form.keys()}
        post_data["user"] = os.environ.get("REMOTE_USER", "unknown")
        headers = {"ApiKey": API_KEY}
        r = requests.post(API_URL, headers=headers, data=post_data, verify=False, allow_redirects=False)
        redirect_url = r.headers.get('Location', '/tags')
        redirect_url = redirect_url.replace('/tags', '/ufl_tag_manager/tags')
        print("Status: 303 See Other")
        print(f"Location: {redirect_url}\n")
        
except Exception as e:
  
    print("Content-Type: text/html\n")
    print(f"<h1>Error: {e}</h1>")

