#!/usr/bin/env python3
import os
print("Content-Type: text/html")
print()
print("<h1>Hello World</h1>")

username = os.environ.get('UFShib_cn')
if username:
    print(f"<h1>Welcome, {username}!</h1>")
else:
    print("<h1>User not authenticated via Shibboleth.</h1>")


print("<table border='1' cellpadding='5'>")
print("<tr><th>Variable</th><th>Value</th></tr>")

for key, value in sorted(os.environ.items()):
    print(f"<tr><td>{key}</td><td>{value}</td></tr>")


