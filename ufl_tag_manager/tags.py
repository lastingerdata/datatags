#!/usr/bin/env python3.9
import cgi
import cgitb; cgitb.enable()
import requests
import os
import certifi
print("Content-Type: text/html\n")
print("")  

API_URL = "https://sushma.lastinger.center.ufl.edu/tags"
API_KEY = 'kdjfghssdujhrjasdfkjasl;kdqwiueqiotru.,sdvmb,mxnvbiuwerfueghb'

method = os.environ.get('REQUEST_METHOD', 'GET').upper()
    
try:
    headers={"ApiKey": API_KEY}
    if method == 'POST':
        form = cgi.FieldStorage()
        post_data = {key:form.getvalue(key) for key in form.keys()}
        r = requests.post(API_URL, headers=headers, data=post_data, verify=False)
    else:
        r = requests.get(API_URL, headers={"ApiKey": API_KEY}, verify=False)
    html = r.text.replace('action="/delete_tag"', 'action="/ufl_tag_manager/delete_tag.py"')
    print(html)

except Exception as e:
    print(f"<h1>Error: {e}</h1>")
