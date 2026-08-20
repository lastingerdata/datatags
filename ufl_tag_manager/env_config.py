#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
from typing import Optional, Set, Dict, Any, List

import requests

ROOT        = os.path.dirname(os.path.abspath(__file__))
ENV_FILE    = os.path.join(ROOT, "env.txt")
CONFIG_FILE = os.path.join(ROOT, "config.json")


def get_environment() -> str:
    try:
        with open(ENV_FILE, "r") as f:
            env_val = f.readline().strip().lower()
            if env_val in ("prod", "test", "local"):
                return env_val
    except Exception:
        pass
    return "local"


def _read_config() -> dict:
    try:
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    except Exception:
        return {}


def get_current_user() -> str:
    user = os.environ.get("REMOTE_USER", "unknown").strip()
    if user and user != "unknown":
        try:
            from libs.login_logs import log_user_login
            log_user_login(user)
        except Exception:
            pass
    return user


# ---------------------------------------------------------------------------
# DB connection helper (shared internally)
# ---------------------------------------------------------------------------

def _db_connect():
    from libs import taggingMySQLDB_connection as localMySQLDB_connection
    return localMySQLDB_connection.LocalDBConnection().connect()


# ---------------------------------------------------------------------------
# Primary access check — replaces VALID_USERS / READ_WRITE_USERS config lists
# ---------------------------------------------------------------------------

def is_in_user_access(user: Optional[str] = None) -> bool:
    """
    Returns True if the user has ANY row in the user_access table.
    This is the single gate for all tagging and dataset pages.
    Users not in the table receive an Access Denied screen.
    """
    user = (user or get_current_user()).strip()
    if not user or user == "unknown":
        return False
    try:
        db = _db_connect()
        cursor = db.cursor(dictionary=True)
        try:
            cursor.execute(
                "SELECT id FROM user_access WHERE LOWER(email) = LOWER(%s) LIMIT 1",
                (user,)
            )
            return cursor.fetchone() is not None
        finally:
            cursor.close()
            db.close()
    except Exception:
        return False


# ---------------------------------------------------------------------------
# Role helpers — all read from user_access DB table
# ---------------------------------------------------------------------------

def get_user_role(user: Optional[str] = None) -> str:
    """
    Returns the user's role from user_access: 'read', 'read_write', or 'admin'.
   
    """
    user = (user or get_current_user()).strip()
    if not user or user == "unknown":
        return "read"
    try:
        db = _db_connect()
        cursor = db.cursor(dictionary=True)
        try:
            cursor.execute(
                "SELECT role FROM user_access WHERE LOWER(email) = LOWER(%s) LIMIT 1",
                (user,)
            )
            row = cursor.fetchone()
            if row and row["role"] in ("read", "read_write", "admin"):
                return row["role"]
        finally:
            cursor.close()
            db.close()
    except Exception:
        pass
    # return "read"
    return None

def has_any_access(user: Optional[str] = None) -> bool:
    return get_user_role(user) is not None


def can_write(user: Optional[str] = None) -> bool:
    """
    Returns True if the user can write tags (role is read_write or admin).
    """
    user = (user or get_current_user()).strip()
    if not user or user == "unknown":
        return False
    return get_user_role(user) in ("read_write", "admin")


def can_edit_tags(user: Optional[str] = None) -> bool:
    """
    Returns True if the user can manage tags (admin only).
    """
    user = (user or get_current_user()).strip()
    if not user or user == "unknown":
        return False
    return get_user_role(user) == "admin"


# ---------------------------------------------------------------------------
# Manager check — still config-based (guards the user_access management page
# itself; 
# ---------------------------------------------------------------------------

def is_manager(user: Optional[str] = None) -> bool:
    """
    Returns True if the user is in the MANAGERS list in config.json.
    Managers can access user_access.py to add/remove users from the DB table.
    Keep MANAGERS in config.json — do NOT move this to the DB table.
    """
    user = (user or get_current_user()).strip()
    if not user or user == "unknown":
        return False
    return user in set(_read_config().get("MANAGERS", []))


# ---------------------------------------------------------------------------

def get_valid_users() -> Set[str]:
    """
    DEPRECATED: access is now controlled by the user_access DB table.
    Use is_in_user_access() instead. Kept only to avoid import errors
    in pages not yet updated.
    """
    return set()


def get_read_write_users() -> Set[str]:
    """
    DEPRECATED: write access is now controlled by get_user_role() via DB.
    Use can_write() instead.
    """
    return set()


def get_tag_admin_users() -> Set[str]:
    """
    DEPRECATED: admin access is now controlled by get_user_role() via DB.
    Use can_edit_tags() instead.
    """
    return set()


# ---------------------------------------------------------------------------
# Admin-only mode — emergency lockdown switch (still config-based)
# ---------------------------------------------------------------------------

def is_admin_only_mode() -> bool:
    """
    Emergency lockdown: when True, only admin-role users can access dataset pages.
    Controlled by ADMIN_ONLY_MODE in config.json.
    """
    data = _read_config()
    return bool(data.get("ADMIN_ONLY_MODE", False))


# ---------------------------------------------------------------------------
# API config
# ---------------------------------------------------------------------------

def get_base_path() -> str:
    env = get_environment()
    if env in ("prod", "test"):
        return "/ufl_tag_manager"
    return "/cgi-bin/ufl_tag_manager"


def get_api_config() -> Dict[str, Any]:
    data = _read_config()
    api  = data.get("API") or {}

    base_url   = (api.get("BASE_URL") or "").strip().rstrip("/")
    verify_ssl = bool(api.get("VERIFY_SSL", False))

    timeout = api.get("TIMEOUT", data.get("API_TIMEOUT", 60))
    try:
        timeout = int(timeout)
    except Exception:
        timeout = 60

    return {
        "base_url":   base_url,
        "timeout":    timeout,
        "verify_ssl": verify_ssl,
    }


def api_url(path: str) -> str:
    cfg  = get_api_config()
    base = cfg["base_url"]
    p    = (path or "").strip()
    if not p.startswith("/"):
        p = "/" + p
    return base + p


def get_api_keys() -> List[str]:
    data = _read_config()
    keys = data.get("API_KEYS") or []
    return [k.strip() for k in keys if isinstance(k, str) and k.strip()]


def get_api_key(index: Optional[int] = None) -> str:
    keys = get_api_keys()
    if not keys:
        return ""
    if index is None:
        return keys[0]
    try:
        return keys[int(index)]
    except Exception:
        return keys[0]


def safe_request(
    url: str,
    method: str = "GET",
    headers: Optional[Dict[str, str]] = None,
    params: Optional[Dict[str, Any]] = None,
    data: Any = None,
    json_body: Any = None,
    verify: Optional[bool] = None,
    timeout: Optional[int] = None,
):
    cfg = get_api_config()
    if verify  is None: verify  = cfg["verify_ssl"]
    if timeout is None: timeout = cfg["timeout"]

    try:
        resp = requests.request(
            method=method, url=url,
            headers=headers or {},
            params=params, data=data,
            json=json_body, timeout=timeout,
            verify=verify,
        )
        return resp
    except Exception as exc:
        return {"error": f"{type(exc).__name__}: {exc}"}


# ---------------------------------------------------------------------------
# MySQL config
# ---------------------------------------------------------------------------

def get_mysql_config() -> Dict[str, Any]:
    data  = _read_config()
    mysql = data.get("MYSQL", {}) or {}
    env   = get_environment().upper()
    cfg   = mysql.get(env, {}) or {}

    port = cfg.get("PORT", 3306)
    try:
        port = int(port)
    except Exception:
        port = 3306

    return {
        "host":     (cfg.get("HOST")     or "").strip(),
        "user":     (cfg.get("USER")     or "").strip(),
        "password":  cfg.get("PASSWORD") or "",
        "database": (cfg.get("DATABASE") or "").strip(),
        "port":      port,
    }


