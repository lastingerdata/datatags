from flask import Blueprint, request, session, redirect, url_for
from functools import wraps

auth_blueprint = Blueprint('auth_blueprint', __name__)

def _get_shibb_user(environ):
    return (environ.get("REDIRECT_REMOTE_USER")
            or environ.get("REMOTE_USER")
            or environ.get("UFShib_eppn")
            or environ.get("UFShib_cn"))

def login_required(view):
    @wraps(view)
    def wrapper(*args, **kwargs):
        user = session.get('user') or _get_shibb_user(request.environ)
        if user:
            session['user'] = user
            return view(*args, **kwargs)
        return redirect(url_for('index'))
    return wrapper
