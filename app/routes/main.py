"""Main routes."""

from flask import Blueprint, redirect, render_template, url_for
from flask_login import current_user, login_required

from app.models.claim import Claim
from app.models.notification import Notification
from app.models.policy import Policy
from app.models.user import User


main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def home():
    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))
    return render_template("home.html")


@main_bp.route("/dashboard")
@login_required
def dashboard():
    notifications = (
        Notification.query.filter_by(user_id=current_user.id).order_by(Notification.created_at.desc()).limit(5)
    )

    if current_user.is_admin():
        total_claims = Claim.query.count()
        approved_claims = Claim.query.filter_by(status="Approved").count()
        pending_claims = Claim.query.filter_by(status="Pending").count()
        return render_template(
            "admin/dashboard.html",
            total_claims=total_claims,
            approved_claims=approved_claims,
            pending_claims=pending_claims,
            users=User.query.order_by(User.created_at.desc()).limit(5),
            policies=Policy.query.order_by(Policy.created_at.desc()).limit(5),
            claims=Claim.query.order_by(Claim.created_at.desc()).limit(10),
            notifications=notifications,
        )

    return render_template(
        "customer/dashboard.html",
        policies=Policy.query.filter_by(customer_id=current_user.id).order_by(Policy.created_at.desc()),
        claims=Claim.query.filter_by(customer_id=current_user.id).order_by(Claim.created_at.desc()),
        notifications=notifications,
    )
