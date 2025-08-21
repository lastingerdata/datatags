import os, json, urllib.parse, urllib.request

API_BASE    = os.environ.get("API_BASE","").rstrip("/")
API_TIMEOUT = float(os.environ.get("API_TIMEOUT","6"))

def _headers(user_email=None):
    h = {"Accept":"application/json"}
    tok = os.environ.get("API_BEARER")
    if tok:
        h["Authorization"] = f"Bearer {tok}"
    if user_email:
        h["X-User-Email"] = user_email
    return h

def get_json(path, params=None, user_email=None):
    if not API_BASE:
        raise RuntimeError("API_BASE not configured")
    url = f"{API_BASE}/{path.lstrip('/')}"
    if params:
        url += "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers=_headers(user_email))
    with urllib.request.urlopen(req, timeout=API_TIMEOUT) as r:
        if r.status != 200:
            raise RuntimeError(f"API error {r.status}")
        return json.loads(r.read().decode("utf-8"))
