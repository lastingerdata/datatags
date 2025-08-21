#!/usr/bin/env python3
import os, cgi, json, urllib.request, urllib.parse

def emit(payload, status=200, ctype="application/json; charset=utf-8"):
    print(f"Status: {status}")
    print(f"Content-Type: {ctype}")
    print()
    print(payload if isinstance(payload, str) else json.dumps(payload, ensure_ascii=False))

def http_get(base, path, params=None, headers=None, timeout=8):
    url = base.rstrip("/") + "/" + path.lstrip("/")
    if params: url += "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers=headers or {"Accept":"application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.headers.get("Content-Type",""), r.read().decode("utf-8")

def main():
    form = cgi.FieldStorage()
    action = (form.getfirst("action","tags") or "tags").strip()
    q      = (form.getfirst("q","") or "").strip()[:100]
    tag_id = (form.getfirst("tag_id","") or "").strip()

    API_BASE = os.environ.get("API_BASE") or "https://tags.lastinger.center.ufl.edu"

    if action == "tags":
        path, params = "/api/tags", {"q": q}                     # e.g. /api/tags?q=math
    elif action == "tag_values":
        path, params = "/api/tag-values", {"tag_id": tag_id}     # e.g. /api/tag-values?tag_id=123
    else:
        emit({"ok": False, "error": "unknown action"}, 400); return

    try:
        user = os.environ.get("REDIRECT_REMOTE_USER") or os.environ.get("REMOTE_USER") or ""
        ctype, body = http_get(API_BASE, path, params, headers={"Accept":"application/json","X-User-Email":user})
        if "json" in ctype.lower():
            emit(json.loads(body))
        else:
            emit(body, 200, ctype or "text/html; charset=utf-8")  # passthrough HTML if your old endpoint returns a page
    except Exception as ex:
        emit({"ok": False, "error": str(ex)}, 500)

if __name__ == "__main__":
    main()

