"""Application factory for Insurance Claim Management System."""

from __future__ import annotations

import os

from flask import Flask

from config import config_by_name

from .extensions import db, login_manager, migrate
from .models import notification, policy, claim, user


def create_app(config_name: str | None = None) -> Flask:
    """Create Flask app using selected configuration."""

    env_name = config_name or os.getenv("FLASK_ENV", "development")
    app = Flask(__name__)
    app.config.from_object(config_by_name.get(env_name, config_by_name["development"]))

    # Ensure runtime folders exist across environments (Windows/Linux/containerized).
    os.makedirs(app.instance_path, exist_ok=True)
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

    database_uri = str(app.config.get("SQLALCHEMY_DATABASE_URI", ""))
    if database_uri.startswith("sqlite:///"):
        sqlite_file_path = database_uri.replace("sqlite:///", "", 1)
        sqlite_parent = os.path.dirname(sqlite_file_path)
        if sqlite_parent:
            os.makedirs(sqlite_parent, exist_ok=True)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    from .routes.auth import auth_bp
    from .routes.main import main_bp
    from .routes.policy import policy_bp
    from .routes.claim import claim_bp
    from .routes.admin import admin_bp
    from .routes.api import api_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(policy_bp)
    app.register_blueprint(claim_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(api_bp, url_prefix="/api")

    return app
