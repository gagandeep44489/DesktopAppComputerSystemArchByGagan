"""Admin routes."""

from flask import Blueprint, render_template

from app.models.claim import Claim
from app.models.policy import Policy
from app.models.user import User
from app.utils import role_required


admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


@admin_bp.route("/users")
@role_required("admin")
def users():
    return render_template("admin/users.html", users=User.query.order_by(User.created_at.desc()))


@admin_bp.route("/policies")
@role_required("admin")
def policies():
    return render_template("admin/policies.html", policies=Policy.query.order_by(Policy.created_at.desc()))


@admin_bp.route("/claims")
@role_required("admin")
def claims():
    return render_template("admin/claims.html", claims=Claim.query.order_by(Claim.created_at.desc()))
