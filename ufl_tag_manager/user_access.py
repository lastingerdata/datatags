#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, cgi, cgitb

from jinja2 import Environment, FileSystemLoader, select_autoescape
from env_config import get_current_user, get_base_path, is_manager, get_user_role
from libs import taggingMySQLDB_connection as localMySQLDB_connection

cgitb.enable()

ROOT = os.path.dirname(os.path.abspath(__file__))
env  = Environment(
    loader=FileSystemLoader(os.path.join(ROOT, "templates")),
    autoescape=select_autoescape(["html", "xml"]),
)

def _connect():
    return localMySQLDB_connection.LocalDBConnection().connect()

def _query(sql, params=(), fetch="all", commit=False):
    db = _connect()
    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute(sql, params)
        if commit:
            db.commit()
            return cursor.lastrowid
        return cursor.fetchall() if fetch == "all" else cursor.fetchone()
    finally:
        cursor.close()
        db.close()

def get_all_users():
    return _query("""
        SELECT id, email, role, added_by, added_at
        FROM user_access ORDER BY added_at DESC
    """)

def add_user(email, role, added_by):
    email = (email or "").strip().lower()
    if not email:
        raise ValueError("Email is required.")
    if role not in ("read", "read_write", "admin"):
        raise ValueError("Role must be 'read', 'read_write', or 'admin'.")
    if _query("SELECT id FROM user_access WHERE LOWER(email) = %s LIMIT 1",
              (email,), fetch="one"):
        raise ValueError(f"User '{email}' already exists.")
    return _query(
        "INSERT INTO user_access (email, role, added_by) VALUES (%s, %s, %s)",
        (email, role, (added_by or "").strip()), commit=True,
    )

def update_user_role(user_id, role):
    if role not in ("read", "read_write", "admin"):
        raise ValueError("Role must be 'read', 'read_write', or 'admin'.")
    _query("UPDATE user_access SET role = %s WHERE id = %s",
           (role, user_id), commit=True)

def remove_user(user_id):
    _query("DELETE FROM user_access WHERE id = %s", (user_id,), commit=True)

def main():
    form         = cgi.FieldStorage()
    method       = os.environ.get("REQUEST_METHOD", "GET").upper()
    current_user = get_current_user()
    user_role    = get_user_role(current_user)
    is_admin     = user_role == "admin"

    if not is_manager(current_user):
        print("Content-Type: text/html; charset=utf-8\n")
        print("<h2>Access Denied</h2><p>You do not have permission to view this page.</p>")
        return

    message = error = ""

    if method == "POST":
        action = form.getfirst("action", "").strip()

        if action == "add":
            try:
                add_user(form.getfirst("email", ""),
                         form.getfirst("role", "read"),
                         added_by=current_user)
                message = f"User '{form.getfirst('email', '').strip().lower()}' added."
            except (ValueError, Exception) as exc:
                error = str(exc)

        elif action == "update":
            try:
                update_user_role(int(form.getfirst("user_id", 0)),
                                 form.getfirst("role", "read"))
                message = "Role updated successfully."
            except (ValueError, Exception) as exc:
                error = str(exc)

        elif action == "remove":
            try:
                remove_user(int(form.getfirst("user_id", 0)))
                message = "User removed successfully."
            except Exception as exc:
                error = f"Failed to remove user: {exc}"

    print("Content-Type: text/html; charset=utf-8\n")
    print(env.get_template("user_access.html").render(
        current_user=current_user,
        base_path=get_base_path(),
        ext=".py",
        page_name="user_access",
        user_role=user_role,
        is_admin=is_admin,
        users=get_all_users(),
        message=message,
        error=error,
    ))


if __name__ == "__main__":
    main()