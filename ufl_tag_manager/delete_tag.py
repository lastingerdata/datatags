#!/usr/bin/env python3.9
import cgi
import cgitb; cgitb.enable()
import requests
import os
import certifi 

API_URL = "https://sushma.lastinger.center.ufl.edu/delete_tag"
API_KEY = 'kdjfghssdujhrjasdfkjasl;kdqwiueqiotru.,sdvmb,mxnvbiuwerfueghb'

method = os.environ.get('REQUEST_METHOD', 'GET').upper()
    
try:
    headers={"ApiKey": API_KEY}
    if method == 'POST':
        form = cgi.FieldStorage()
        post_data = {key:form.getvalue(key) for key in form.keys()}
        r = requests.post(API_URL, headers=headers, data=post_data, verify=False)
    print("Status: 303 See Other")
    print("Location: /ufl_tag_manager/tags.py\n")

except Exception as e:
    print(f"<h1>Error: {e}</h1>")
