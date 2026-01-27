import os
import sys
import json
import requests
from typing import Optional
 
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
            print(f"DEBUG: Environment from env.txt = {env_val}", file=sys.stderr)
            return env_val
    except Exception as e:
        print(f"DEBUG: Failed reading env.txt ({e}); defaulting to 'local'.", file=sys.stderr)
        return "local"
 
 
def get_api_key() -> Optional[str]:
 
    env = get_environment()
    try:
        with open(CONFIG_FILE, "r") as f:
            data = json.load(f)
    except Exception as e:
        print(f"DEBUG: Failed reading config.json ({e}); returning None.", file=sys.stderr)
        return None
 
    api_key = data.get("API_KEY")
    valid_users = data.get("VALID_USERS", [])
 
    if env == "local":
        return api_key
 
    user = os.environ.get("REMOTE_USER", "unknown")
 
    if user in valid_users:
        return api_key
 
    return None
 
def api_base() -> str:
   
    env = get_environment()
    if env == "prod":
        base = PROD_API_BASE
    elif env == "local":
        base = TEST_API_BASE
    else:
        base = TEST_API_BASE
 
    return base
 
 
def api_url(path: str) -> str:
   
    base = api_base().rstrip("/")
    return f"{base}/{path.lstrip('/')}"


def get_base_path() -> str:
    """
    Returns the base path for CGI scripts based on environment.
    - local: /cgi-bin/ufl_tag_manager (includes cgi-bin prefix for local development)
    - prod: /ufl_tag_manager (no cgi-bin prefix in production)
    """
    env = get_environment()
    if env in("prod","test"):
        return "/ufl_tag_manager"
    else:
        return "/cgi-bin/ufl_tag_manager"
 
 
def safe_request(url: Optional[str], method: str = "GET", **kwargs):
 
    url = url or api_url("")
    try:
        response = requests.request(method, url, timeout=10, **kwargs)
 
        if response.status_code in (401, 403):
            return {
                "error": "Access restricted. Please contact Sushma (su.palle@ufl.edu)."
            }
        elif response.status_code == 409:
            return response
 
        response.raise_for_status()
        return response
 
    except requests.exceptions.ConnectionError:
        return {
            "error": (
                "Unable to connect to test API. This is expected if the server is off. "
                "Contact Sushma (su.palle@ufl.edu)."
            )
        }
    except requests.RequestException as e:
 
        return {"error": f"Request error: {e}"}