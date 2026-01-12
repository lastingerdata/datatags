#!/usr/bin/env python3

import os
import sys
import cgi
import cgitb
import traceback
import urllib.parse

cgitb.enable()

from jinja2 import Environment, FileSystemLoader, select_autoescape
from env_config import api_url, get_api_key, safe_request, get_base_path

ROOT = os.path.dirname(os.path.abspath(__file__))
TEMPLATES = os.path.join(ROOT, "templates")

env = Environment(
    loader=FileSystemLoader(TEMPLATES),
    autoescape=select_autoescape(["html", "xml"])
)

BASE_PATH = get_base_path()
EXT = ".py"

API_KEY = "kdjfghssdujhrjasdfkjasl;kdqwiueqiotru.,sdvmb,mxnvbiuwerfueghb"

def print_headers(content_type="text/html; charset=utf-8", status=None, extra=None):
    if status:
        print(f"Status: {status}")
    print(f"Content-Type: {content_type}")
    if extra:
        for k, v in extra.items():
            print(f"{k}: {v}")
    print()


def redirect_with_messages(messages):
    import time
    pairs = [("m", f"{c}:{t}") for c, t in messages]
    # Add timestamp to prevent caching
    pairs.append(("_t", str(int(time.time() * 1000))))
    qs = urllib.parse.urlencode(pairs)
    redirect_url = f"{BASE_PATH}/tags{EXT}" + (f"?{qs}" if qs else "")
    extra = {
        "Cache-Control": "no-store, no-cache, must-revalidate, max-age=0",
        "Pragma": "no-cache",
        "Location": redirect_url
    }
    print_headers(status="303 See Other", extra=extra)
    # Print a simple redirect page body for browsers that don't auto-follow
    print(f'<!DOCTYPE html><html><head><meta http-equiv="refresh" content="0;url={redirect_url}"></head><body>Redirecting...</body></html>')


def parse_messages_from_qs():
    messages = []
    qs = os.environ.get("QUERY_STRING", "")
    if not qs:
        return messages

    for v in urllib.parse.parse_qs(qs, keep_blank_values=True).get("m", []):
        if ":" in v:
            c, t = v.split(":", 1)
            messages.append((c, t))

    return messages


def _read_text(resp, limit=500):
    try:
        return (getattr(resp, "text", "") or "")[:limit]
    except Exception:
        return ""


def fetch_tags_json():
    """
    Mirrors Flask /tags?format=json:
      returns list or {"data": list}
    """
    import re
    
    headers = {
        "Accept": "application/json",
        "ApiKey": API_KEY
    }

    resp = safe_request(api_url("/tags?format=json"), headers=headers, verify=False)

    if isinstance(resp, dict):
        raise RuntimeError(resp.get("error", "API Error"))

    status = getattr(resp, "status_code", None)

    if status and not (200 <= status < 300):
        body = _read_text(resp)
        raise RuntimeError(f"Backend {status}: {body}")

    # Try to parse as JSON first
    try:
        data = resp.json()
        if isinstance(data, dict) and "data" in data:
            data = data["data"]

        if isinstance(data, list):
            return data
    except Exception:
        pass  # Fall back to HTML parsing
    
    # Fallback: Parse HTML response if JSON parsing failed
    html = resp.text
    tags = []
    
    # Extract tag data from HTML using regex
    tag_blocks = re.findall(
        r'<div id="row-(\d+)".*?<span class="tag-name"[^>]*>\s*(.*?)\s*</span>.*?<span id="desc-\1"[^>]*>\s*(.*?)\s*</span>',
        html,
        re.DOTALL
    )
    
    if tag_blocks:
        for tag_id, tag_name, desc_block in tag_blocks:
            # Extract description from the desc block
            desc_match = re.search(r'\(Description:\s*(.*?)\s*\)', desc_block)
            description = desc_match.group(1) if desc_match else ""
            
            # Clean up HTML entities
            tag_name = tag_name.strip()
            description = description.replace('&#39;', "'").replace('&#34;', '"').replace('&lt;', '<').replace('&gt;', '>')
            
            tags.append({
                "tag_id": int(tag_id),
                "tag_name": tag_name,
                "description": description
            })
        
        return tags
    
    # Neither JSON nor HTML parsing worked
    body = _read_text(resp)
    raise RuntimeError(
        f"Backend returned unexpected response format. Body: {body}"
    )


def add_tag(name, desc, user):
   
    headers = {
        "Accept": "application/json",
        "ApiKey": API_KEY
    }

    payload = {
        "tag_name": name,
        "description": desc,
        "user": user
    }

    resp = safe_request(
        api_url("/tags"),
        method="POST",
        headers=headers,
        data=payload,
        verify=False
    )

    if isinstance(resp, dict) and resp.get("error"):
        raise RuntimeError(resp["error"])

    sc = getattr(resp, "status_code", 200)
    if not (200 <= sc < 400):
        raise RuntimeError(f"Add failed ({sc}): {_read_text(resp)}")


def delete_tag(tag_id, user):
    
    headers = {"Accept": "text/html,application/json", "ApiKey": API_KEY, "X-API-Key": API_KEY}

    payload = {
        "tag_id": tag_id, "user": user
    }

    resp = safe_request(
        api_url("/delete_tag"),
        method="POST",
        headers=headers,
        data=payload,
        verify=False
    )

    if isinstance(resp, dict) and resp.get("error"):
        raise RuntimeError(resp["error"])

    sc = getattr(resp, "status_code", 0)
    if not (200 <= sc < 400):
        raise RuntimeError(f"Delete HTTP failed ({sc}): {_read_text(resp)}")

    final_url = getattr(resp, "url", "") or ""
    location = resp.headers.get("Location", "") or ""
    body = _read_text(resp)

    marker = f"{api_url('/tags')}"
    combined = " ".join([final_url, location, body])

   
    if "deleted=0" in combined or "Cannot delete tag (likely has associated values)" in combined:
        raise RuntimeError("Cannot delete tag (likely has associated values)")
    


def main():
    try:
        method = os.environ.get("REQUEST_METHOD", "GET").upper()
        user = (
            os.environ.get("REMOTE_USER", "")
            or os.environ.get("HTTP_REMOTE_USER", "")
            or "unknown"
        )

        if method == "POST":
            form = cgi.FieldStorage()
            action = (form.getfirst("action") or "").lower()
            messages = []

            try:
                if action == "add":
                    name = (form.getfirst("tag_name") or "").strip()
                    desc = (form.getfirst("description") or "").strip()

                    if not name:
                        messages.append(("danger", "Tag name required"))
                    else:
                        add_tag(name, desc, user)
                        messages.append(("success", f"Tag '{name}' added"))

                elif action == "delete":
                    tag_id = (form.getfirst("tag_id") or "").strip()
                    tag_name = (form.getfirst("tag_name") or "").strip()

                    if not tag_id:
                        messages.append(("danger", "Missing tag_id for delete"))
                    else:
                        delete_tag(tag_id, user)
                        label = tag_name or f"ID {tag_id}"
                        messages.append(("success", f"Tag {label} deleted"))

                else:
                    messages.append(("danger", "Unknown action"))

            except Exception as e:
                messages.append(("danger", f"Operation failed: {e}"))

            return redirect_with_messages(messages)

      
        messages = parse_messages_from_qs()

        try:
            tags = fetch_tags_json()
        except Exception as e:
            tags = []
            messages.append(("danger", f"Failed to load tags: {e}"))

        html = env.get_template("tags.html").render(
            base_path=BASE_PATH,
            ext=EXT,
            tags=tags,
            messages=messages,
            user=user,
            page_name='tags'
        )

        print_headers(extra={
            "Cache-Control": "no-store, no-cache, must-revalidate, max-age=0",
            "Pragma": "no-cache",
            "Expires": "0"
        })
        sys.stdout.write(html)

    except Exception:
        print_headers()
        esc = (
            traceback.format_exc()
            .replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
        )
        sys.stdout.write(f"<h1>tags.py crashed</h1><pre>{esc}</pre>")

if __name__ == "__main__":
    main()