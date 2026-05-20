#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import cgi
import cgitb

from jinja2 import Environment, FileSystemLoader, select_autoescape
from env_config import get_current_user, get_base_path, is_manager
from libs import taggingMySQLDB_connection as localMySQLDB_connection

cgitb.enable()

ROOT = os.path.dirname(os.path.abspath(__file__))
env = Environment(
    loader=FileSystemLoader(os.path.join(ROOT, "templates")),
    autoescape=select_autoescape(["html", "xml"]),
)


# ---------------------------------------------------------------------------
# DB helpers  (user_access table)
# ---------------------------------------------------------------------------

def _connect():
    return localMySQLDB_connection.LocalDBConnection().connect()


def get_all_users():
    db = _connect()
    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT id, email, role, added_by, added_at
            FROM user_access
            ORDER BY added_at DESC
        """)
        return cursor.fetchall()
    finally:
        cursor.close()
        db.close()


def add_user(email, role, added_by):
    email = (email or "").strip().lower()
    if not email:
        raise ValueError("Email is required.")
    if role not in ("read", "read_write", "admin"):
        raise ValueError("Role must be 'read', 'read_write', or 'admin'.")

    db = _connect()
    cursor = db.cursor()
    try:
        cursor.execute(
            "SELECT id FROM user_access WHERE LOWER(email) = %s LIMIT 1",
            (email,)
        )
        if cursor.fetchone():
            raise ValueError(f"User '{email}' already exists.")

        cursor.execute(
            "INSERT INTO user_access (email, role, added_by) VALUES (%s, %s, %s)",
            (email, role, (added_by or "").strip())
        )
        db.commit()
        return cursor.lastrowid
    finally:
        cursor.close()
        db.close()


def update_user_role(user_id, role):
    if role not in ("read", "read_write", "admin"):
        raise ValueError("Role must be 'read', 'read_write', or 'admin'.")

    db = _connect()
    cursor = db.cursor()
    try:
        cursor.execute(
            "UPDATE user_access SET role = %s WHERE id = %s",
            (role, user_id)
        )
        db.commit()
        return cursor.rowcount > 0
    finally:
        cursor.close()
        db.close()


def remove_user(user_id):
    db = _connect()
    cursor = db.cursor()
    try:
        cursor.execute("DELETE FROM user_access WHERE id = %s", (user_id,))
        db.commit()
        return cursor.rowcount > 0
    finally:
        cursor.close()
        db.close()

def main():

    # current_user = get_current_user()
    # print("Content-Type: text/html; charset=utf-8\n")
    # print(f"<pre>current_user = '{current_user}'</pre>")
    # return 

    form         = cgi.FieldStorage()
    method       = os.environ.get("REQUEST_METHOD", "GET").upper()
    current_user = get_current_user()

    # Access guard — managers only
    if not is_manager(current_user):
        print("Content-Type: text/html; charset=utf-8\n")
        print("<h2>Access Denied</h2><p>You do not have permission to view this page.</p>")
        return

    message = ""
    error   = ""

    if method == "POST":
        action = form.getfirst("action", "").strip()

        if action == "add":
            email = form.getfirst("email", "").strip().lower()
            role  = form.getfirst("role",  "read").strip()
            try:
                add_user(email, role, added_by=current_user)
                message = f"User '{email}' added with role '{role}'."
            except ValueError as exc:
                error = str(exc)
            except Exception as exc:
                error = f"Failed to add user: {exc}"

        elif action == "update":
            user_id = form.getfirst("user_id", "").strip()
            role    = form.getfirst("role", "read").strip()
            try:
                update_user_role(int(user_id), role)
                message = "Role updated successfully."
            except ValueError as exc:
                error = str(exc)
            except Exception as exc:
                error = f"Failed to update role: {exc}"

        elif action == "remove":
            user_id = form.getfirst("user_id", "").strip()
            try:
                remove_user(int(user_id))
                message = "User removed successfully."
            except Exception as exc:
                error = f"Failed to remove user: {exc}"

    users = get_all_users()

    print("Content-Type: text/html; charset=utf-8\n")
    print(env.get_template("user_access.html").render(
        current_user=current_user,
        base_path=get_base_path(),
        ext=".py",
        page_name="user_access",
        users=users,
        message=message,
        error=error,
    ))


if __name__ == "__main__":
    main()