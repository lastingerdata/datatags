#!/usr/bin/env python3
# -*- coding: utf-8 -*-
 
import os
import re
import cgitb
 
from jinja2 import Environment, FileSystemLoader, select_autoescape
from env_config import (
    get_current_user, get_base_path, get_api_key, get_user_role, safe_request,
    is_in_user_access, is_admin_only_mode,
)
 
cgitb.enable()
 
ROOT = os.path.dirname(os.path.abspath(__file__))
env  = Environment(
    loader=FileSystemLoader(os.path.join(ROOT, "templates")),
    autoescape=select_autoescape(["html", "xml"]),
)
 
SWAGGER_DOCS_URL = "https://compute.lastinger.center.ufl.edu/swagger_docs"
GITHUB_BASE_URL = "https://github.com/lastingerdata/reporting/blob/master/python/root/libs/cached_core_libs"
 
 
def render(template_name, **kwargs):
    print("Content-Type: text/html; charset=utf-8\n")
    print(env.get_template(template_name).render(**kwargs))
 
 
def render_access_denied(current_user):
    render("dataset_description.html",
        current_user=current_user,
        base_path=get_base_path(),
        page_name="dataset_description",
        access_denied=True,
        user_role="read",
        datasets=[],
        has_git_access=False,
        ext=".py",
    )
 
 
def fetch_swagger_docs():
    try:
        resp = safe_request(
            SWAGGER_DOCS_URL,
            headers={"Accept": "application/json", "ApiKey": get_api_key(2)},
            verify=False,
        )
        if isinstance(resp, (dict, list)):
            return resp
        return resp.json()
    except Exception as exc:
        return {"_error": str(exc)}
 
 
def build_datasets(swagger_docs):
 
    datasets = []
 
    if not isinstance(swagger_docs, list):
        return datasets
 
    for item in swagger_docs:
        if not isinstance(item, dict):
            continue
 
        for endpoint_name, data in item.items():
            if not isinstance(data, dict):
                continue
 
            # Only show endpoints flagged
            if not data.get("x-show_on_website"):
                continue
 
            questions = []
            for q in (data.get("x-questions") or []):
                q = re.sub(r"^\d+\.\s*", "", str(q)).strip()
                if q:
                    questions.append(q)
 
            # Columns — from responses > 200 > examples > application/json
            columns = []
            try:
                col_block = data["responses"]["200"]["examples"]["application/json"]
                if isinstance(col_block, dict):
                    for col_name, meta in col_block.items():
                        if not isinstance(meta, dict):
                            continue
 
                        raw_ex = meta.get("Examples")
                        if isinstance(raw_ex, list):
                            example = ", ".join(
                                str(e).strip() for e in raw_ex
                                if e is not None and str(e).strip()
                            )
                        elif raw_ex and str(raw_ex).strip():
                            example = str(raw_ex).strip()
                        else:
                            example = ""
 
                        anon = str(meta.get("Anonymized") or "false").strip().lower() == "true"
 
                        columns.append({
                            "col":     col_name.strip(),
                            "desc":    (meta.get("description") or "").strip(),
                            "anon":    anon,
                            "example": example,
                        })
            except (KeyError, TypeError):
                pass
 
            clean_name = endpoint_name.replace("-", "_")
 
            datasets.append({
                "name":        endpoint_name.upper(),
                "title":       " ".join(p.capitalize() for p in endpoint_name.split("_") if p),
                "description": " ".join((data.get("description") or "").split()),
                "questions":   questions,
                "columns":     columns,
                "doc_link":    f"{GITHUB_BASE_URL}/{clean_name}_dict.py",
            })
 
    datasets.sort(key=lambda d: d["name"])
    return datasets
 
 
def main():
    current_user = get_current_user()

    is_admin = get_user_role(current_user) == "admin"
    is_valid = is_in_user_access(current_user)

    # ADMIN_ONLY_MODE = emergency lockdown (only admins can access)
    # Normal mode     = anyone in the user_access table can view the guide
    if (is_admin_only_mode() and not is_admin) or (not is_admin_only_mode() and not is_valid):
        render_access_denied(current_user)
        return
 
    swagger_docs = fetch_swagger_docs()
 
    if isinstance(swagger_docs, dict) and "_error" in swagger_docs:
        datasets = []
    else:
        datasets = build_datasets(swagger_docs)
 
    render("dataset_description.html",
        current_user=current_user,
        base_path=get_base_path(),
        ext=".py",
        page_name="dataset_description",
        access_denied=False,
        user_role=get_user_role(current_user),
        datasets=datasets,
    )
 
 
if __name__ == "__main__":
    main()