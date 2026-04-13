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
                dataset_description, nightly_refresh
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

def get_all_dataset_requests():
    db = localMySQLDB_connection.LocalDBConnection().connect()
    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT
                request_id, endpoint, table_name, schema_name,
                headers_json, requested_by, status,
                created_at, updated_at, error_message,
                dataset_description, nightly_refresh
            FROM dataset_requests
            ORDER BY request_id DESC
        """)
        return cursor.fetchall()
    finally:
        cursor.close()
        db.close()


def add_request(endpoint, table_name, schema_name, headers_json,
                        requested_by, dataset_description="", nightly_refresh=False):
   
    endpoint, table_name, schema_name, headers_json = _normalize_dataset_key(
        endpoint, table_name, schema_name, headers_json
    )
    db = localMySQLDB_connection.LocalDBConnection().connect()
    cursor = db.cursor()
    try:
        cursor.execute("""
            INSERT INTO dataset_requests
                (endpoint, table_name, schema_name, headers_json,
                 requested_by, status, dataset_description, nightly_refresh)
            VALUES (%s, %s, %s, %s, %s, 'pending', %s, %s)
        """, (
            endpoint, table_name, schema_name, headers_json,
            (requested_by or "").strip(),
            (dataset_description or "").strip(),
            1 if nightly_refresh else 0,
        ))
        db.commit()
        return cursor.lastrowid
    finally:
        cursor.close()
        db.close()


def refresh_existing_request(request_id):
    """
    Resets an existing completed/failed request back to pending so the
    Snowflake processor picks it up and re-runs it.
    Only allowed when current status is 'completed' or 'failed'.
    """
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
    """
    Toggles the nightly_refresh flag for an existing request (admin only).
    nightly_refresh: True/False or 1/0
    """
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
    return {"result": "REFRESH_REQUESTED", "request_id": new_request_id,
            "message": "Refresh requested successfully.",
            "existing_request": decision["existing_request"]}



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