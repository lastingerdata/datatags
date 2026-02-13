import os
import sys
import json
import requests
from typing import Optional, Set, List

ROOT = os.path.dirname(os.path.abspath(__file__))

ENV_FILE = os.path.join(ROOT, "env.txt")
CONFIG_FILE = os.path.join(ROOT, "config.json")

TEST_API_BASE = "https://sushma.lastinger.center.ufl.edu"
PROD_API_BASE = "https://compute.lastinger.center.ufl.edu"


def get_environment() -> str:
    try:
        with open(ENV_FILE, "r") as f:
            env_val = f.readline().strip().lower()
            if not env_val:
                raise ValueError("env.txt is empty")
            return env_val
    except Exception:
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
    data = _read_config()
    return set(data.get("VALID_USERS", []))


def get_read_write_users() -> Set[str]:
    data = _read_config()
    return set(data.get("READ_WRITE_USERS", []))


def can_write(user: Optional[str] = None) -> bool:
    user = user or get_current_user()
    return user in get_read_write_users()


def get_api_keys() -> List[str]:
    data = _read_config()
    keys = data.get("API_KEYS")
    if isinstance(keys, list) and keys:
        return [str(k) for k in keys if k]
    single = data.get("API_KEY")
    if isinstance(single, str) and single.strip():
        return [single.strip()]
    return []


def get_api_key(index: int = 0) -> Optional[str]:
    env = get_environment()
    keys = get_api_keys()
    if not keys:
        return None
    if index < 0 or index >= len(keys):
        return None
    key = keys[index]
    if env == "local":
        return key
    user = get_current_user()
    if user in get_valid_users():
        return key
    return None


def get_api_timeout(default: int = 10) -> int:
    data = _read_config()
    try:
        return int(data.get("API_TIMEOUT", default))
    except Exception:
        return default


def api_base() -> str:
    env = get_environment()
    if env == "prod":
        return PROD_API_BASE
    return TEST_API_BASE


def api_url(path: str) -> str:
    base = api_base().rstrip("/")
    return f"{base}/{path.lstrip('/')}"


def get_base_path() -> str:
    env = get_environment()
    if env in ("prod", "test"):
        return "/ufl_tag_manager"
    return "/cgi-bin/ufl_tag_manager"


def safe_request(url: Optional[str], method: str = "GET", **kwargs):
    url = url or api_url("")
    timeout = kwargs.pop("timeout", get_api_timeout(10))
    try:
        response = requests.request(method, url, timeout=timeout, **kwargs)
        if response.status_code in (401, 403):
            return {"error": "Access restricted. Please contact Sushma (su.palle@ufl.edu)."}
        if response.status_code == 409:
            return response
        response.raise_for_status()
        return response
    except requests.exceptions.ConnectionError:
        return {"error": "Unable to connect to test API. Contact Sushma (su.palle@ufl.edu)."}
    except requests.RequestException as e:
        return {"error": f"Request error: {e}"}
