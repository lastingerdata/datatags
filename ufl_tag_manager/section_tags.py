#!/usr/bin/env python3
import os
import cgitb
import requests
import certifi

cgitb.enable()

print("Content-Type: text/html\n")

API_URL = "https://sushma.lastinger.center.ufl.edu/section_tags"
API_KEY = "your-api-key"
headers = {"ApiKey": API_KEY}

query_string = os.environ.get("QUERY_STRING", "")
full_url = API_URL + "?" + query_string if query_string else API_URL

try:
    r = requests.get(full_url, headers=headers, verify=False)
    html = r.text

    html = html.replace('href="/"', 'href="/ufl_tag_manager/home.py"')
    html = html.replace('action="/section_tags_inserts"', 'action="/ufl_tag_manager/add_section_tags.py"')
    html = html.replace('action="/delete_section_tag"', 'action="/ufl_tag_manager/delete_section_tag.py"')
    html = html.replace('action="/delete_selected_section_tags"', 'action="/ufl_tag_manager/delete_selected_section_tags.py"')

    print(html)

except Exception as e:
    print(f"<h1 style='color:red;'>Error: {e}</h1>")

# #!/usr/bin/env python3.9
# import cgi
# import cgitb; cgitb.enable()
# import requests
# import os
# # print("Content-Type: text/plain; charset=utf-8")
# # print("")  

# API_URL = "https://sushma.lastinger.center.ufl.edu/section_tags"
# API_KEY = 'kdjfghssdujhrjasdfkjasl;kdqwiueqiotru.,sdvmb,mxnvbiuwerfueghb'

# method = os.environ.get('REQUEST_METHOD', 'GET').upper()
# headers = {"ApiKey": API_KEY}

# try:
#     if method == "POST":
#         form = cgi.FieldStorage()
#         post_data = {key: form.getvalue(key) for key in form.keys()}
#         post_data["user"] = os.environ.get("REMOTE_USER", "unknown")
    
#         response = requests.post(API_URL, headers=headers, data=post_data, verify=False)
#         section_id = form.getvalue("section_id", "")
#         if response.ok and section_id:
#             redirect_url = f"/ufl_tag_manager/section_tags.py?section_id={section_id}"
#             print("Status: 303 See Other")
#             print(f"Location: {redirect_url}\n")
#         elif not response.ok:
#             print("Content-Type: text/html\n")

#             print(f"<h1 style='color:red;'>API Error: {response.status_code}</h1>")
#         else:
#             print("Content-Type: text/html\n")

#             print("<h1 style='color:red;'>Missing section_id for redirect </h1>")
#     else:
      
#         query_string = os.environ.get("QUERY_STRING", "")
#         url = API_URL + "?" + query_string if query_string else API_URL
#         response = requests.get(url, headers=headers, verify=False)


#     html = response.text

#     html = html.replace('href="/"', 'href="/ufl_tag_manager/home.py"')
#     html = html.replace('action="/section_tags"', 'action="/ufl_tag_manager/section_tags.py"')
#     html = html.replace('action="/delete_section_tag"', 'action="/ufl_tag_manager/delete_section_tag.py"')

#     print(html)

# except Exception as e:
#     print(f"<h1 style='color:red;'>Error: {e}</h1>")