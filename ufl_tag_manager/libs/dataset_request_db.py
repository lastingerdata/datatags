#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from libs import taggingMySQLDB_connection as localMySQLDB_connection

DEFAULT_SEGMENT_VALUES = [
    "Academic Year 2022-23",
    "Academic Year 2023-24",
    "Academic Year 2024-25",
    "Academic Year 2025-26",
]

def normalize_headers(headers_json):
    if not headers_json or not str(headers_json).strip():
        return ""
    try:
        return json.dumps(
            json.loads(headers_json),
            sort_keys=True,
            separators=(",", ":")
        )
    except (json.JSONDecodeError, TypeError):
        return str(headers_json).strip()

def _normalize_dataset_key(endpoint, table_name, schema_name, headers_json):
    return (
        (endpoint or "").strip(),
        (table_name or "").strip().upper(),
        (schema_name or "").strip().lower(),
        normalize_headers(headers_json),
    )

# ─────────────────────────────────────────────────────────────────────────────
# EXISTING REQUEST LOOKUPS
# ─────────────────────────────────────────────────────────────────────────────

def get_existing_request(endpoint, table_name, schema_name, headers_json):
    endpoint, table_name, schema_name, headers_json = _normalize_dataset_key(
        endpoint, table_name, schema_name, headers_json
    )
    db = localMySQLDB_connection.LocalDBConnection().connect()
    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT
                request_id, endpoint, table_name, schema_name,
                headers_json, requested_by, status,
                created_at, updated_at, error_message,
                dataset_description, nightly_refresh, owner_type
            FROM dataset_requests
            WHERE endpoint = %s
              AND table_name = %s
              AND schema_name = %s
              AND COALESCE(headers_json, '') = %s
            ORDER BY created_at DESC, request_id DESC
            LIMIT 1
        """, (endpoint, table_name, schema_name, headers_json))
        return cursor.fetchone()
    finally:
        cursor.close()
        db.close()

def get_existing_status(endpoint, table_name, schema_name, headers_json):
    row = get_existing_request(endpoint, table_name, schema_name, headers_json)
    return row["status"] if row else None


# ─────────────────────────────────────────────────────────────────────────────
# ADMIN LIST — admin-owned requests with optional filters + pagination
# Used by: dataset_requests_list.py (admin only page)
# ─────────────────────────────────────────────────────────────────────────────

def get_admin_requests(endpoint_filter=None, table_filter=None,
                       header_filter=None, page=1, page_size=25):
    """
    Returns only owner_type='admin' rows.
    Optionally filter by endpoint name, table name, or headers (text search).
    Paginated — page starts at 1.
    Also returns total count for pagination controls.
    """
    offset = (page - 1) * page_size

    where_clauses = ["owner_type = 'admin'"]
    params = []

    if endpoint_filter:
        where_clauses.append("endpoint = %s")
        params.append(endpoint_filter.strip())

    if table_filter:
        where_clauses.append("table_name LIKE %s")
        params.append(f"%{table_filter.strip().upper()}%")

    if header_filter:
        where_clauses.append("headers_json LIKE %s")
        params.append(f"%{header_filter.strip()}%")

    where_sql = " AND ".join(where_clauses)

    db = localMySQLDB_connection.LocalDBConnection().connect()
    cursor = db.cursor(dictionary=True)
    try:
        # Total count for pagination
        cursor.execute(f"""
            SELECT COUNT(*) AS total FROM dataset_requests
            WHERE {where_sql}
        """, params)
        total = cursor.fetchone()["total"]

        # Paginated rows
        cursor.execute(f"""
            SELECT
                request_id, endpoint, table_name, schema_name,
                headers_json, requested_by, status,
                created_at, updated_at, error_message,
                dataset_description, nightly_refresh, owner_type
            FROM dataset_requests
            WHERE {where_sql}
            ORDER BY request_id DESC
            LIMIT %s OFFSET %s
        """, params + [page_size, offset])

        rows = cursor.fetchall()
        return rows, total
    finally:
        cursor.close()
        db.close()


# ─────────────────────────────────────────────────────────────────────────────
# USER LIST — requests for a specific user, paginated
# Used by: my_datasets.py
# ─────────────────────────────────────────────────────────────────────────────

def get_user_requests(current_user, is_admin=False, page=1, page_size=25):
    """
    For regular users  → only their own owner_type='user' rows
    For admins         → ALL owner_type='user' rows (every user's requests)
    Paginated — page starts at 1.
    Also returns total count for pagination controls.
    """
    offset = (page - 1) * page_size

    if is_admin:
        where_sql = "owner_type = 'user'"
        params = []
    else:
        where_sql = "owner_type = 'user' AND LOWER(requested_by) = LOWER(%s)"
        params = [(current_user or "").strip()]

    db = localMySQLDB_connection.LocalDBConnection().connect()
    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute(f"""
            SELECT COUNT(*) AS total FROM dataset_requests
            WHERE {where_sql}
        """, params)
        total = cursor.fetchone()["total"]

        cursor.execute(f"""
            SELECT
                request_id, endpoint, table_name, schema_name,
                headers_json, requested_by, status,
                created_at, updated_at, error_message,
                dataset_description, nightly_refresh, owner_type
            FROM dataset_requests
            WHERE {where_sql}
            ORDER BY request_id DESC
            LIMIT %s OFFSET %s
        """, params + [page_size, offset])

        rows = cursor.fetchall()
        return rows, total
    finally:
        cursor.close()
        db.close()


# ─────────────────────────────────────────────────────────────────────────────
# BACKWARDS COMPATIBILITY
# ─────────────────────────────────────────────────────────────────────────────

def get_all_dataset_requests():
    db = localMySQLDB_connection.LocalDBConnection().connect()
    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT
                request_id, endpoint, table_name, schema_name,
                headers_json, requested_by, status,
                created_at, updated_at, error_message,
                dataset_description, nightly_refresh, owner_type
            FROM dataset_requests
            ORDER BY request_id DESC
        """)
        return cursor.fetchall()
    finally:
        cursor.close()
        db.close()


# ─────────────────────────────────────────────────────────────────────────────
# INSERT
# ─────────────────────────────────────────────────────────────────────────────

def add_request(endpoint, table_name, schema_name, headers_json,
                requested_by, dataset_description="", nightly_refresh=False,
                owner_type="admin"):
    """
    owner_type = 'admin' → admin-created shared dataset (default)
    owner_type = 'user'  → user-requested personal dataset
    """
    endpoint, table_name, schema_name, headers_json = _normalize_dataset_key(
        endpoint, table_name, schema_name, headers_json
    )
    db = localMySQLDB_connection.LocalDBConnection().connect()
    cursor = db.cursor()
    try:
        cursor.execute("""
            INSERT INTO dataset_requests
                (endpoint, table_name, schema_name, headers_json,
                 requested_by, status, dataset_description,
                 nightly_refresh, owner_type)
            VALUES (%s, %s, %s, %s, %s, 'pending', %s, %s, %s)
        """, (
            endpoint, table_name, schema_name, headers_json,
            (requested_by or "").strip(),
            (dataset_description or "").strip(),
            1 if nightly_refresh else 0,
            owner_type if owner_type in ("admin", "user") else "admin",
        ))
        db.commit()
        return cursor.lastrowid
    finally:
        cursor.close()
        db.close()


# ─────────────────────────────────────────────────────────────────────────────
# REFRESH / UPDATE HELPERS
# ─────────────────────────────────────────────────────────────────────────────

def refresh_existing_request(request_id):
    db = localMySQLDB_connection.LocalDBConnection().connect()
    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute(
            "SELECT status FROM dataset_requests WHERE request_id = %s",
            (request_id,)
        )
        row = cursor.fetchone()
        if not row:
            raise ValueError(f"No request found with ID {request_id}.")

        status = (row.get("status") or "").strip().lower()
        if status in ("pending", "processing"):
            raise ValueError(f"Cannot refresh — request is currently {status}.")

        cursor.execute("""
            UPDATE dataset_requests
            SET status = 'pending',
                error_message = NULL,
                updated_at = NOW()
            WHERE request_id = %s
        """, (request_id,))
        db.commit()
        return True
    finally:
        cursor.close()
        db.close()


def set_nightly_refresh(request_id, nightly_refresh):
    db = localMySQLDB_connection.LocalDBConnection().connect()
    cursor = db.cursor()
    try:
        cursor.execute("""
            UPDATE dataset_requests
            SET nightly_refresh = %s,
                updated_at = NOW()
            WHERE request_id = %s
        """, (1 if nightly_refresh else 0, request_id))
        db.commit()
        return True
    finally:
        cursor.close()
        db.close()


def request_refresh(endpoint, table_name, schema_name, headers_json,
                    requested_by, dataset_description=""):
    decision = get_request_action(endpoint, table_name, schema_name, headers_json)
    action = decision["action"]

    if action in ("BLOCK_PENDING", "BLOCK_PROCESSING"):
        raise ValueError(decision["message"])
    if action == "NEW_REQUEST":
        raise ValueError("No existing completed or failed dataset request was found to refresh.")

    new_request_id = add_request(
        endpoint=endpoint, table_name=table_name, schema_name=schema_name,
        headers_json=headers_json, requested_by=requested_by,
        dataset_description=dataset_description,
    )
    return {
        "result": "REFRESH_REQUESTED",
        "request_id": new_request_id,
        "message": "Refresh requested successfully.",
        "existing_request": decision["existing_request"],
    }


# ─────────────────────────────────────────────────────────────────────────────
# TABLE EXISTS CHECK
# ─────────────────────────────────────────────────────────────────────────────

def table_exists(table_name, schema_name):
    db = localMySQLDB_connection.LocalDBConnection().connect()
    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT request_id FROM dataset_requests
            WHERE table_name = %s
              AND schema_name = %s
            LIMIT 1
        """, (
            (table_name or "").strip().upper(),
            (schema_name or "").strip().lower(),
        ))
        return cursor.fetchone() is not None
    finally:
        cursor.close()
        db.close()


# ─────────────────────────────────────────────────────────────────────────────
# TAG / SEGMENT HELPERS
# ─────────────────────────────────────────────────────────────────────────────

def get_all_tags():
    db = localMySQLDB_connection.LocalDBConnection().connect()
    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute("SELECT tag_name FROM ufl_tags ORDER BY tag_name ASC")
        return [row["tag_name"] for row in cursor.fetchall()]
    finally:
        cursor.close()
        db.close()


def get_tag_values_by_tag(tag_name):
    if not tag_name:
        return []
    db = localMySQLDB_connection.LocalDBConnection().connect()
    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT tv.tag_value
            FROM ufl_tag_values tv
            INNER JOIN ufl_tags t ON tv.tag_id = t.tag_id
            WHERE t.tag_name = %s
            ORDER BY tv.tag_value ASC
        """, (tag_name,))
        return [row["tag_value"] for row in cursor.fetchall()]
    finally:
        cursor.close()
        db.close()


def get_segment_values():
    db = localMySQLDB_connection.LocalDBConnection().connect()
    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT tag_value FROM ufl_tag_values
            WHERE tag_id = 12
            ORDER BY tag_value ASC
        """)
        values = [row["tag_value"] for row in cursor.fetchall() if row.get("tag_value")]
        return values if values else DEFAULT_SEGMENT_VALUES
    finally:
        cursor.close()
        db.close()


def edit_request(request_id, table_name=None, dataset_description=None, schema_name=None):
    """
    Update the editable metadata fields of a dataset request.
    Only table_name, dataset_description, and schema_name can be changed.
    Headers/endpoint are not editable — those require a new request.
    """
    fields  = []
    params  = []

    if table_name is not None:
        table_name = table_name.strip().upper()
        if not table_name:
            raise ValueError("Table name cannot be empty.")
        fields.append("table_name = %s")
        params.append(table_name)

    if dataset_description is not None:
        fields.append("dataset_description = %s")
        params.append(dataset_description.strip())

    if schema_name is not None:
        schema_name = schema_name.strip().lower()
        if not schema_name:
            raise ValueError("Schema name cannot be empty.")
        fields.append("schema_name = %s")
        params.append(schema_name)

    if not fields:
        raise ValueError("No fields provided to update.")

    fields.append("updated_at = NOW()")
    params.append(int(request_id))

    db = localMySQLDB_connection.LocalDBConnection().connect()
    cursor = db.cursor()
    try:
        cursor.execute(
            f"UPDATE dataset_requests SET {', '.join(fields)} WHERE request_id = %s",
            params,
        )
        db.commit()
        if cursor.rowcount == 0:
            raise ValueError(f"Request #{request_id} not found.")
    finally:
        cursor.close()
        db.close()


def delete_request(request_id):
    """
    Permanently delete a dataset request by ID.
    Admin only — enforced at the view layer.
    """
    db = localMySQLDB_connection.LocalDBConnection().connect()
    cursor = db.cursor()
    try:
        cursor.execute(
            "DELETE FROM dataset_requests WHERE request_id = %s",
            (int(request_id),),
        )
        db.commit()
        if cursor.rowcount == 0:
            raise ValueError(f"Request #{request_id} not found.")
    finally:
        cursor.close()
        db.close()