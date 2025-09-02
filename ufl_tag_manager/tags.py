#!/usr/bin/env python3.9
import cgi
import cgitb; cgitb.enable()
import requests
import os

print("Content-Type: text/html\n")

# print("Content-Type: text/plain; charset=utf-8")
# print("")  

API_URL = "https://sushma.lastinger.center.ufl.edu/tags"
API_KEY = 'kdjfghssdujhrjasdfkjasl;kdqwiueqiotru.,sdvmb,mxnvbiuwerfueghb'

method = os.environ.get('REQUEST_METHOD', 'GET').upper()

try:
    headers={"ApiKey": API_KEY}
    if method == 'POST':
        form = cgi.FieldStorage()
        post_data = {key:form.getvalue(key) for key in form.keys()}
        post_data["user"] = os.environ.get("REMOTE_USER", "unknown")
        r = requests.post(API_URL, headers=headers, data=post_data, verify=False)
    else:
        query_string = os.environ.get("QUERY_STRING", "")
        url = API_URL + "?" + query_string if query_string else API_URL
        r = requests.get(url, headers=headers, verify=False)
    html = r.text
    html = html.replace('href="/"', 'href="/ufl_tag_manager/home.py"')
    html = html.replace('action="/delete_tag"', 'action="/ufl_tag_manager/delete_tag.py"')
    print(html)

except Exception as e:
    print(f"<h1>Error: {e}</h1>")







# #!/usr/bin/env python3
# import cgi
# import cgitb
# import requests
# import os

# cgitb.enable()

# print("Content-Type: text/html\n")

# API_URL = "https://sushma.lastinger.center.ufl.edu/tags"
# API_KEY = "kdjfghssdujhrjasdfkjasl;kdqwiueqiotru.,sdvmb,mxnvbiuwerfueghb"

# method = os.environ.get("REQUEST_METHOD", "GET").upper()
# headers = {"ApiKey": API_KEY}

# try:
#     if method == "POST":
#         form = cgi.FieldStorage()
#         post_data = {key: form.getvalue(key) for key in form.keys()}
#         post_data["user"] = os.environ.get("REMOTE_USER", "unknown")

#         r = requests.post(API_URL, headers=headers, data=post_data, verify=False)
#     else:
#         query_string = os.environ.get("QUERY_STRING", "")
#         url = API_URL + "?" + query_string if query_string else API_URL
#         r = requests.get(url, headers=headers, verify=False)

#     html = r.text

#     # ✅ Check for flash message based on redirect query
#     flash_message = ""
#     query = os.environ.get("QUERY_STRING", "")
#     if "deleted=1" in query:
#         flash_message = '<div style="color: green; font-weight: bold;">Tag deleted successfully.</div>'
#     elif "deleted=0" in query:
#         flash_message = '<div style="color: red; font-weight: bold;">Failed to delete tag.</div>'

#     # ✅ Inject flash message into HTML
#     html = html.replace("<body>", f"<body>{flash_message}", 1)

#     # ✅ Update form and href actions for CGI
#     html = html.replace('href="/', 'href="/ufl_tag_manager/home.py"')
#     html = html.replace('action="/delete_tag"', 'action="/ufl_tag_manager/delete_tag.py"')
#     html = html.replace('action="/tags"', 'action="/ufl_tag_manager/tags.py"')

#     print(html)

# except Exception as e:
#     print(f"<h1 style='color:red;'>Error: {e}</h1>")