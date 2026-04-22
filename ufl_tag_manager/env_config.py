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
    return os.environ.get("REMOTE_USER", "unknown").strip()


def get_valid_users() -> Set[str]:
    """
    Used only for dataset requests access control(just for testing phase).
    """
    data = _read_config()
    return set(data.get("VALID_USERS", []))


def get_read_write_users() -> Set[str]:
    data = _read_config()
    return set(data.get("READ_WRITE_USERS", []))


def can_write(user: Optional[str] = None) -> bool:
    """
    Controls write access to the tagging pages (section tags, bulk inserts etc).
    Any authenticated UF user (passed Shibboleth login) can write.
    We only block unauthenticated / unknown users.
    """
    user = (user or get_current_user()).strip()
    return user in get_read_write_users()
    # return bool(user) and user != "unknown"


def get_tag_admin_users() -> Set[str]:
    data = _read_config()
    return set(data.get("TAG_ADMIN_USERS", []))


def can_edit_tags(user: Optional[str] = None) -> bool:
    """
    Controls admin-level tag management (add/delete tags and tag values).
    Restricted to TAG_ADMIN_USERS in config.json.
    """
    user = (user or get_current_user())
    return user in get_tag_admin_users()


def get_base_path() -> str:
    env = get_environment()
    if env in ("prod", "test"):
        return "/ufl_tag_manager"
    return "/cgi-bin/ufl_tag_manager"


def get_api_config() -> Dict[str, Any]:
    data = _read_config()
    api  = data.get("API") or {}

    base_url  = (api.get("BASE_URL") or "").strip().rstrip("/")
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
            method=method,
            url=url,
            headers=headers or {},
            params=params,
            data=data,
            json=json_body,
            timeout=timeout,
            verify=verify,
        )
        return resp
    except Exception as exc:
        return {"error": f"{type(exc).__name__}: {exc}"}


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


def is_admin_only_mode() -> bool:
    """
    lockdown switch for dataset pages.
    When True, only TAG_ADMIN_USERS can access dataset pages.
    Controlled by ADMIN_ONLY_MODE in config.json.
    """
    data = _read_config()
    return bool(data.get("ADMIN_ONLY_MODE", False))