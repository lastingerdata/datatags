#!/usr/bin/env python3
import os
import cgi
import cgitb
import requests

cgitb.enable()

API_URL = "https://sushma.lastinger.center.ufl.edu/delete_tag"

API_KEY = 'kdjfghssdujhrjasdfkjasl;kdqwiueqiotru.,sdvmb,mxnvbiuwerfueghb'

method = os.environ.get("REQUEST_METHOD", "GET").upper()

try:
    if method == "POST":
        form = cgi.FieldStorage()
        post_data = {key: form.getvalue(key) for key in form.keys()}
        post_data["user"] = os.environ.get("REMOTE_USER", "unknown")
        headers = {"ApiKey": API_KEY}       
        r = requests.post(API_URL, headers=headers, data=post_data, verify=False, allow_redirects=False)

        if r.status_code == 200:
            print("Status: 303 See Other")
            print("Location: /ufl_tag_manager/tags.py?deleted=1\n") 
        else:
            print("Status: 303 See Other")
            print("Location: /ufl_tag_manager/tags.py?deleted=0\n")
        
except Exception as e:
  
    print("Content-Type: text/html\n")
    print(f"<h1>Error: {e}</h1>")


# #!/usr/bin/env python3
# import os
# import cgi
# import cgitb
# import requests
# import certifi

# cgitb.enable()

# # print("Content-Type: text/html\n")

# API_URL = "https://sushma.lastinger.center.ufl.edu/delete_tag"
# API_KEY = "kdjfghssdujhrjasdfkjasl;kdqwiueqiotru.,sdvmb,mxnvbiuwerfueghb"

# method = os.environ.get("REQUEST_METHOD", "GET").upper()

# try:
#     if method == "POST":
#         form = cgi.FieldStorage()
#         tag_id = form.getvalue("tag_id")
#         user = os.environ.get("REMOTE_USER", "unknown")

#         if tag_id:
#             post_data = {
#                 "tag_id": tag_id,
#                 "user": user
#             }
#             headers = {"ApiKey": API_KEY}

#             # 🔁 POST to backend
#             r = requests.post(API_URL, headers=headers, data=post_data, verify=certifi.where())

#             # ✅ Redirect to tags.py with success/failure flag
#             if r.status_code == 200:
#                 print("Status: 303 See Other")
#                 print("Location: /ufl_tag_manager/tags.py?deleted=1\n")
#             else:
#                 print("Status: 303 See Other")
#                 print("Location: /ufl_tag_manager/tags.py?deleted=0\n")
#         else:
#             print("Status: 303 See Other")
#             print("Location: /ufl_tag_manager/tags.py?deleted=0\n")

#     else:
#         print("Content-Type: text/html\n")
#         print("<h1>Invalid request method</h1>")

# except Exception as e:
#     print("Status: 303 See Other")
#     print("Location: /ufl_tag_manager/tags.py?deleted=0\n")
