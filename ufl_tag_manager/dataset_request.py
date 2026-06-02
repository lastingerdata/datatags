#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, re, cgi, cgitb, json

from jinja2 import Environment, FileSystemLoader, select_autoescape
from env_config import (
    get_current_user, get_base_path, get_api_key, safe_request,
    get_user_role, is_in_user_access, is_admin_only_mode,
)
from libs.dataset_request_db import (
    add_request, request_refresh, get_existing_status, get_all_tags,
    get_tag_values_by_tag, get_segment_values, table_exists,
)

cgitb.enable()

ROOT = os.path.dirname(os.path.abspath(__file__))
env  = Environment(
    loader=FileSystemLoader(os.path.join(ROOT, "templates")),
    autoescape=select_autoescape(["html", "xml"]),
)

SWAGGER_DOCS_URL        = "https://compute.lastinger.center.ufl.edu/swagger_docs"
SNOWFLAKE_IDENTIFIER_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_$]{0,254}$")

_TYPE_MAP = {
    "int": "int", "integer": "int",
    "bool": "boolean", "boolean": "boolean",
    "json": "json", "array": "array", "object": "object",
}


def render(template_name, **kwargs):
    print("Content-Type: text/html; charset=utf-8\n")
    print(env.get_template(template_name).render(**kwargs))


def render_access_denied(current_user):
    render("dataset_request.html",
        current_user=current_user, base_path=get_base_path(),
        page_name="dataset_request", access_denied=True,
        schema_name="", derived_schema="", is_admin=False,
        user_role="read",
        message="", error="", warn_refresh=False, prefill={},
        endpoint_list=[], endpoint_map_json="{}", swagger_error="",
        ext=".py", prefill_headers_json="[]", segment_values_json="[]",
        all_tags_json="[]", all_tag_values_json="{}",
    )


def derive_schema_name(email):
    return re.sub(r"[^a-zA-Z0-9]", "", (email or "").split("@")[0]).lower()


def validate_schema_name(name):
    name = (name or "").strip().lower()
    if not name:
        return False, "Schema name is required."
    if not SNOWFLAKE_IDENTIFIER_RE.fullmatch(name):
        return False, (
            "Schema name must start with a letter or _, and may only contain "
            "letters, numbers, _, or $. No spaces or special characters."
        )
    return True, ""


def validate_table_name(name):
    name = (name or "").strip()
    if not name:
        return False, "Table name is required."
    if len(name) > 255:
        return False, "Table name must be 255 characters or fewer."
    if not SNOWFLAKE_IDENTIFIER_RE.fullmatch(name):
        return False, (
            "Table name must start with a letter or _, and may only contain "
            "letters, numbers, _, or $. No spaces or special characters."
        )
    return True, ""


def empty_prefill():
    return {
        "endpoint": "", "table_name": "", "dataset_description": "",
        "submitted_headers": [], "nightly_refresh": False, "schema_name": "",
    }


def fetch_swagger_docs():
    try:
        resp = safe_request(
            SWAGGER_DOCS_URL,
            headers={"Accept": "application/json", "ApiKey": get_api_key(2)},
            verify=False,
        )
        if isinstance(resp, (dict, list)):
            return resp
        try:
            return resp.json()
        except Exception:
            return json.loads(getattr(resp, "text", "") or "{}")
    except Exception as exc:
        return {"_error": str(exc)}


def parse_dataset_endpoints(swagger_docs):
    endpoint_map = {}
    if isinstance(swagger_docs, list):
        for item in swagger_docs:
            if not isinstance(item, dict):
                continue
            for name, data in item.items():
                clean = (name or "").lstrip("/").strip()
                if not clean:
                    continue
                data = data if isinstance(data, dict) else {}
                if not data.get("x-show_on_website"):
                    continue
                endpoint_map[clean] = {
                    "description": data.get("description") or "",
                    "parameters":  data.get("parameters") or [],
                    "responses":   data.get("responses") or {},
                }
    return endpoint_map


def normalize_type(raw):
    return _TYPE_MAP.get((raw or "string").strip().lower(), "string")


def get_header_params(endpoint_data):
    result = []
    for p in endpoint_data.get("parameters") or []:
        if not isinstance(p, dict) or p.get("in") != "header" or not p.get("name"):
            continue
        raw_type = p.get("type") or (p.get("schema") or {}).get("type")
        result.append({
            "name":        p["name"].strip(),
            "type":        normalize_type(raw_type),
            "required":    bool(p.get("required")),
            "description": p.get("description") or "",
        })
    return result


def validate_header(param, raw):
    name  = param["name"]
    ptype = param["type"]
    raw   = "" if raw is None else str(raw).strip()

    if not raw:
        return True, None, ""

    try:
        if ptype == "string": return True, raw, ""
        if ptype == "int":    return True, int(raw), ""
        if ptype == "boolean":
            if raw.lower() in ("true", "1", "yes"):  return True, "true", ""
            if raw.lower() in ("false", "0", "no"):  return True, "false", ""
            return False, None, f"Header '{name}' must be true or false."
        if ptype in ("json", "array", "object"):
            parsed = json.loads(raw)
            if ptype == "array"  and not isinstance(parsed, list): return False, None, f"Header '{name}' must be a JSON array."
            if ptype == "object" and not isinstance(parsed, dict): return False, None, f"Header '{name}' must be a JSON object."
            return True, parsed, ""
        return True, raw, ""
    except (ValueError, json.JSONDecodeError):
        return False, None, f"Header '{name}' must be valid {ptype}."


def build_headers_json(endpoint_data, form):
    errors    = []
    headers   = {}
    param_map = {p["name"]: p for p in get_header_params(endpoint_data)}

    names  = form.getlist("header_name")
    values = form.getlist("header_value")
    seen   = set()

    for i, raw_name in enumerate(names):
        name  = (raw_name or "").strip()
        value = values[i] if i < len(values) else ""
        if not name:
            continue
        if name in seen:
            errors.append(f"Header '{name}' was added more than once.")
            continue
        seen.add(name)

        if name not in param_map:
            errors.append(f"Invalid header '{name}' for this endpoint.")
            continue

        ok, coerced, err = validate_header(param_map[name], value)
        if not ok:
            errors.append(err)
        elif coerced is not None:
            headers[name] = coerced

    for p in param_map.values():
        if p["required"] and p["name"] not in headers:
            errors.append(f"Required header '{p['name']}' is missing.")

    return headers, errors


def main():
    form         = cgi.FieldStorage()
    method       = os.environ.get("REQUEST_METHOD", "GET").upper()
    current_user = get_current_user()

    is_admin = get_user_role(current_user) == "admin"
    is_valid = is_in_user_access(current_user)

    # dataset_request.py is admin-only regardless of ADMIN_ONLY_MODE.
    # Only admins can submit dataset requests.
    if not is_valid:
        render_access_denied(current_user)
        return

    derived_schema = derive_schema_name(current_user)

    swagger_docs  = fetch_swagger_docs()
    swagger_error = ""

    if isinstance(swagger_docs, dict) and "_error" in swagger_docs:
        swagger_error = swagger_docs["_error"]
        endpoint_map  = {}
    else:
        endpoint_map = parse_dataset_endpoints(swagger_docs)

    endpoint_list  = sorted(endpoint_map)
    segment_values = get_segment_values()
    all_tags       = get_all_tags()
    all_tag_values = {tag: get_tag_values_by_tag(tag) for tag in all_tags}

    query_ep  = form.getfirst("ep", "").strip()
    ep_lookup = {ep.lower(): ep for ep in endpoint_list}
    prefill   = {
        **empty_prefill(),
        "endpoint":    ep_lookup.get(query_ep.lower(), ""),
        "schema_name": derived_schema,
    }

    message      = ""
    error        = ""
    warn_refresh = False

    if method == "POST":
        action              = form.getfirst("action",    "submit").strip()
        endpoint            = form.getfirst("endpoint",  "").strip()
        table_name          = form.getfirst("table_name", "").strip()
        dataset_description = form.getfirst("dataset_description", "").strip()
        nightly_refresh     = False

        if is_admin:
            nightly_refresh = form.getfirst("nightly_refresh", "0").strip() == "1"
            schema_name     = (form.getfirst("schema_name", "") or "").strip().lower() or derived_schema
        else:
            schema_name = derived_schema

        names  = form.getlist("header_name")
        values = form.getlist("header_value")
        submitted_headers = [
            {"name": (names[i] or "").strip(), "value": values[i] if i < len(values) else ""}
            for i in range(len(names))
            if (names[i] or "").strip() or (values[i] if i < len(values) else "")
        ]

        prefill = {
            "endpoint":            endpoint,
            "table_name":          table_name,
            "dataset_description": dataset_description,
            "submitted_headers":   submitted_headers,
            "nightly_refresh":     nightly_refresh,
            "schema_name":         schema_name,
        }

        if swagger_error:
            error = f"Endpoint list could not be loaded: {swagger_error}"
        elif not endpoint or not table_name:
            error = "Endpoint and table name are required."
        elif endpoint not in endpoint_map:
            error = "Please select a valid endpoint."
        else:
            valid_schema, schema_err = validate_schema_name(schema_name)
            if not valid_schema:
                error = schema_err
            else:
                valid_table, table_err = validate_table_name(table_name)
                if not valid_table:
                    error = table_err
                else:
                    if action != "refresh" and table_exists(table_name.upper(), schema_name):
                        error = (
                            f"Table '{table_name.upper()}' already exists in schema '{schema_name}'. "
                            f"Please choose a different table name."
                        )
                    else:
                        headers_obj, header_errors = build_headers_json(endpoint_map[endpoint], form)
                        if header_errors:
                            error = " ".join(header_errors)
                        else:
                            headers_json = json.dumps(headers_obj, sort_keys=True)

                            if action == "refresh":
                                try:
                                    request_refresh(
                                        endpoint, table_name.upper(), schema_name,
                                        headers_json, current_user, dataset_description,
                                    )
                                    message = f"Refresh requested for {schema_name}.{table_name.upper()}"
                                    prefill = {**empty_prefill(), "schema_name": schema_name}
                                except Exception as exc:
                                    error = str(exc)

                            else:
                                status = get_existing_status(
                                    endpoint, table_name.upper(), schema_name, headers_json
                                )
                                if status in ("pending", "processing"):
                                    error = f"Request already {status}. Please wait."
                                elif status == "completed":
                                    warn_refresh = True
                                    error = f"{schema_name}.{table_name.upper()} already exists."
                                else:
                                    try:
                                        owner_type = "admin" if is_admin else "user"
                                        add_request(
                                            endpoint, table_name.upper(), schema_name,
                                            headers_json, current_user, dataset_description,
                                            nightly_refresh=nightly_refresh,
                                            owner_type=owner_type,
                                        )
                                        message = f"Request submitted for {schema_name}.{table_name.upper()}"
                                        prefill = {**empty_prefill(), "schema_name": schema_name}
                                    except Exception as exc:
                                        error = f"Failed to save request: {exc}"

    render("dataset_request.html",
        current_user=current_user,
        schema_name=prefill.get("schema_name", derived_schema),
        derived_schema=derived_schema,
        is_admin=is_admin,
        user_role=get_user_role(current_user),
        access_denied=False,
        message=message,
        error=error,
        warn_refresh=warn_refresh,
        prefill=prefill,
        endpoint_list=endpoint_list,
        endpoint_map_json=json.dumps(endpoint_map),
        swagger_error=swagger_error,
        page_name="dataset_request",
        base_path=get_base_path(),
        ext=".py",
        prefill_headers_json=json.dumps(prefill.get("submitted_headers", [])),
        segment_values_json=json.dumps(segment_values),
        all_tags_json=json.dumps(all_tags),
        all_tag_values_json=json.dumps(all_tag_values),
    )

if __name__ == "__main__":
    main()