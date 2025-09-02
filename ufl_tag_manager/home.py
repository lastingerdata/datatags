#!/usr/bin/env python3.9
import cgi
import cgitb; cgitb.enable()
import requests
import os
print("Content-Type: text/html; charset=utf-8")
# print("Content-Type: text/html\n")
print("")  

API_URL = "https://sushma.lastinger.center.ufl.edu/"
API_KEY = 'kdjfghssdujhrjasdfkjasl;kdqwiueqiotru.,sdvmb,mxnvbiuwerfueghb'
PDF_URL = "/ufl_tag_manager/assets/Tagging%20website%20Documentation.pdf"

try:
    headers = {"ApiKey": API_KEY}
    r = requests.get(API_URL, headers=headers, verify=False)
    html = r.text
    html = html.replace('href="/"', 'href="/ufl_tag_manager/home.py"')
    html = html.replace('/section_tags_inserts"', '/ufl_tag_manager/section_tags_inserts.py"')
    html = html.replace('/section_tags"', '/ufl_tag_manager/section_tags.py"')
    html = html.replace('/tag_values"', '/ufl_tag_manager/tag_values.py"')
    html = html.replace('/tags', '/ufl_tag_manager/tags.py"')
    html = html.replace('/static/docs/Tagging%20website%20Documentation.pdf', PDF_URL)\
    .replace('href="#"', f'href="{PDF_URL}" target="_blank" rel="noopener"')\
    .replace('>About</a>', f' target="_blank" rel="noopener" href="{PDF_URL}">About</a>')
     

    print(html)

except Exception as e:
    print(f"<h1>Error: {e}</h1>")

