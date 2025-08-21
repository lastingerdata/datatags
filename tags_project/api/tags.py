#!/usr/bin/env python3
import os, json, cgi, cgitb
cgitb.enable()

API_BASE = os.environ.get("API_BASE","").rstrip("/")
TIMEOUT  = float(os.environ.get("API_TIMEOUT","6"))

def current_user():
    e = os.environ
    return (e.get("REDIRECT_REMOTE_USER") or e.get("REMOTE_USER")
            or e.get("UFShib_eppn") or e.get("UFShib_cn") or "unknown@ufl.edu")

def _headers():
    h = {"Accept":"application/json", "X-User-Email": current_user()}
    token = os.environ.get("API_BEARER")
    if token: h["Authorization"] = f"Bearer {token}"
    return h

def json_out(payload, status=200):
    print(f"Status: {status}")
    print("Content-Type: application/json; charset=utf-8")
    print()
    print(json.dumps(payload, ensure_ascii=False))

def method(): return os.environ.get("REQUEST_METHOD","GET").upper()

def form():
    fs = cgi.FieldStorage()
    return {k: fs.getvalue(k) for k in (fs.keys() or [])}

def proxy_get():
    import requests
    if not API_BASE: return json_out({"ok":False,"error":"API_BASE not set"},500)
    r = requests.get(f"{API_BASE}/tags", headers=_headers(), timeout=TIMEOUT)
    return json_out(_try_json(r), r.status_code)

def proxy_post():
    import requests
    if not API_BASE: return json_out({"ok":False,"error":"API_BASE not set"},500)
    data = form()  # expects tag_name, description
    r = requests.post(f"{API_BASE}/tags", headers=_headers(), json=data, timeout=TIMEOUT)
    return json_out(_try_json(r), r.status_code)

def _try_json(resp):
    try: return resp.json()
    except Exception: return {"ok":False,"status":resp.status_code,"text":resp.text[:500]}

def main():
    m = method()
    if m == "GET":  return proxy_get()
    if m == "POST": return proxy_post()
    return json_out({"ok":False,"error":"Method Not Allowed"},405)

if __name__ == "__main__":
    main()
