#!/usr/bin/env python3
import argparse
import ast
import json

from libs.dataset_request_db import add_request, get_existing_status

try:
    from env_config import get_api_key, safe_request
except ImportError:
    get_api_key = None
    safe_request = None

SWAGGER_URL = "https://compute.lastinger.center.ufl.edu/swagger_docs"
SCHEMA_NAME = "final"
REQUESTED_BY = "su.palle@ufl.edu"


# ---------- Step 1: read the dataset entries out of the file ----------

def get_dataset_entries(file_path):
    with open(file_path, "r") as f:
        file_text = f.read()

    tree = ast.parse(file_text)
    entries = []

    for node in ast.walk(tree):
        if not isinstance(node, ast.Dict):
            continue

        entry = {"endpoint": None, "table_name": None, "headers": {}}
        for key_node, value_node in zip(node.keys, node.values):
            if not isinstance(key_node, ast.Constant):
                continue
            key = key_node.value

            if key == "EndPoint":
                entry["endpoint"] = safe_literal(value_node)
            elif key == "TableName":
                entry["table_name"] = safe_literal(value_node)
            elif key == "headers":
                entry["headers"] = safe_literal(value_node) or {}

        if entry["endpoint"] and entry["table_name"]:
            entries.append(entry)

    return entries


def safe_literal(value_node):
    try:
        return ast.literal_eval(value_node)
    except Exception:
        return None


# ---------- Step 2: get descriptions from the swagger docs website ----------

def get_swagger_descriptions():
    if safe_request is None or get_api_key is None:
        print("no descriptions available.")
        return {}

    try:
        response = safe_request(
            SWAGGER_URL,
            headers={"Accept": "application/json", "ApiKey": get_api_key(2)},
            verify=False,
        )
        data = response if isinstance(response, (list, dict)) else response.json()
    except Exception as exc:
        print(f"Could not reach swagger docs ({exc}). No descriptions available.")
        return {}

    descriptions = {}
    if isinstance(data, list):
        for item in data:
            for name, info in item.items():
                descriptions[name] = info.get("description", "")
    elif isinstance(data, dict):
        for name, info in data.items():
            descriptions[name] = info.get("description", "")

    return descriptions


# ---------- Step 3: insert everything ----------

def run(file_path, dry_run):
    entries = get_dataset_entries(file_path)

    if not entries:
        print("No dataset entries found.")
        return

    descriptions = get_swagger_descriptions()

    inserted = 0
    skipped_duplicates = 0
    skipped_no_description = 0

    for entry in entries:
        endpoint = entry["endpoint"]
        table_name = entry["table_name"].upper()
        headers_json = json.dumps(entry["headers"], sort_keys=True)
        description = descriptions.get(endpoint)

        if not description:
            print(f"SKIP (no description found for '{endpoint}'): {table_name}")
            skipped_no_description += 1
            continue

        already_exists = get_existing_status(endpoint, table_name, SCHEMA_NAME, headers_json)
        if already_exists:
            print(f"SKIP (already exists, status={already_exists}): {table_name}")
            skipped_duplicates += 1
            continue

        if dry_run:
            print(f"WOULD INSERT: {table_name}")
        else:
            add_request(
                endpoint, table_name, SCHEMA_NAME, headers_json,
                REQUESTED_BY, description, True, "admin",
            )
            print(f"INSERTED: {table_name}")
        inserted += 1

    print("-" * 60)
    print(f"{'Would insert' if dry_run else 'Inserted'}: {inserted}")
    print(f"Skipped (duplicates): {skipped_duplicates}")
    print(f"Skipped (no description): {skipped_no_description}")


def main():
    parser = argparse.ArgumentParser(description="Bulk-add dataset requests.")
    parser.add_argument("--file", required=True, help="Path to the batch file")
    parser.add_argument("--dry-run", action="store_true",
                         help="Preview only -- don't actually insert anything")
    args = parser.parse_args()
    run(args.file, args.dry_run)


if __name__ == "__main__":
    main()