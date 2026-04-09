"""Utility helpers for validation and access control."""

from __future__ import annotations

import uuid
from datetime import datetime
from functools import wraps
from pathlib import Path

from flask import abort, current_app, flash, redirect, request, url_for
from flask_login import current_user
from werkzeug.utils import secure_filename


def role_required(*roles):
    """Decorator to restrict access by role."""

    def decorator(fn):
        @wraps(fn)
        def wrapped(*args, **kwargs):
            if not current_user.is_authenticated:
                return redirect(url_for("auth.login"))
            if current_user.role not in roles:
                abort(403)
            return fn(*args, **kwargs)

        return wrapped

    return decorator


def allowed_file(filename: str) -> bool:
    if "." not in filename:
        return False
    ext = filename.rsplit(".", 1)[1].lower()
    return ext in current_app.config["ALLOWED_EXTENSIONS"]


def save_uploaded_document(file_storage):
    """Save upload with unique filename after extension validation."""

    if not file_storage or file_storage.filename == "":
        return None

    if not allowed_file(file_storage.filename):
        flash("Only PNG/JPG/PDF documents are allowed.", "danger")
        return None

    ext = file_storage.filename.rsplit(".", 1)[1].lower()
    safe_name = secure_filename(file_storage.filename)
    unique_name = f"{uuid.uuid4().hex}_{safe_name}"
    destination = Path(current_app.config["UPLOAD_FOLDER"]) / unique_name
    file_storage.save(destination)
    return unique_name


def parse_date(value: str):
    """Parse YYYY-MM-DD string into date object."""

    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except ValueError:
        return None
