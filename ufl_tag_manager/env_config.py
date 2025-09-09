
import os, json, requests

ROOT = os.path.dirname(os.path.abspath(__file__))
ENV_FILE = os.path.join(ROOT, '.env')

TEST_API_BASE = "https://sushma.lastinger.center.ufl.edu"
PROD_API_BASE = "https://tags.lastinger.center.ufl.edu"

def get_api_key() -> str:
    user = os.environ.get("REMOTE_USER", "unknown")
    try:
        with open("config.json", 'r') as f:
            data = json.load(f)
            API_KEY = data["API_KEY"]
            VALID_USERS = data["VALID_USERS"]
            if user in VALID_USERS:
                return API_KEY
            else:
                return None
    except Exception:
        return None

def api_base():
    try:
        with open(ENV_FILE, 'r') as f:
            lines = f.readlines()
            env = lines[0].strip().lower()
    except Exception:  
        env = 'test'
    return PROD_API_BASE if env == 'prod' else TEST_API_BASE

def api_url(path: str) -> str:
    base = api_base().rstrip("/")
    return f"{base}/{path.lstrip('/')}"

def safe_request(url: str, **kwargs):
    try:
        response = requests.get(url, timeout=10, **kwargs)
        response.raise_for_status()
        return response
    except requests.exceptions.RequestException:
        return {"error": "Unable to connect to test API. This is expected if the server is off, Contact Sushma(su.palle@ufl.edu)"}
