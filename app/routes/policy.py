"""Policy management routes."""

from __future__ import annotations

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from app.extensions import db
from app.models.policy import Policy
from app.models.user import User
from app.utils import parse_date, role_required


policy_bp = Blueprint("policy", __name__, url_prefix="/policies")


@policy_bp.route("/")
@login_required
def list_policies():
    if current_user.is_admin():
        policies = Policy.query.order_by(Policy.created_at.desc())
    else:
        policies = Policy.query.filter_by(customer_id=current_user.id).order_by(Policy.created_at.desc())
    return render_template("policies/list.html", policies=policies)


@policy_bp.route("/new", methods=["GET", "POST"])
@role_required("admin")
def create_policy():
    customers = User.query.filter_by(role="customer").order_by(User.full_name.asc())
    if request.method == "POST":
        policy_number = request.form.get("policy_number", "").strip()
        policy_type = request.form.get("policy_type", "").strip()
        premium = request.form.get("premium", "0").strip()
        valid_from = parse_date(request.form.get("valid_from", ""))
        valid_to = parse_date(request.form.get("valid_to", ""))
        customer_id = request.form.get("customer_id", "")

        if not all([policy_number, policy_type, valid_from, valid_to, customer_id]):
            flash("All fields are required.", "danger")
            return render_template("policies/form.html", customers=customers)

        if valid_to < valid_from:
            flash("Policy end date cannot be earlier than start date.", "danger")
            return render_template("policies/form.html", customers=customers)

        try:
            premium_value = float(premium)
            assert premium_value > 0
        except (ValueError, AssertionError):
            flash("Premium must be a positive number.", "danger")
            return render_template("policies/form.html", customers=customers)

        if Policy.query.filter_by(policy_number=policy_number).first():
            flash("Policy number already exists.", "warning")
            return render_template("policies/form.html", customers=customers)

        policy = Policy(
            policy_number=policy_number,
            policy_type=policy_type,
            premium=premium_value,
            valid_from=valid_from,
            valid_to=valid_to,
            customer_id=int(customer_id),
        )
        db.session.add(policy)
        db.session.commit()
        flash("Policy created successfully.", "success")
        return redirect(url_for("policy.list_policies"))

    return render_template("policies/form.html", customers=customers)


@policy_bp.route("/<int:policy_id>/edit", methods=["GET", "POST"])
@role_required("admin")
def edit_policy(policy_id: int):
    policy = Policy.query.get_or_404(policy_id)
    customers = User.query.filter_by(role="customer").order_by(User.full_name.asc())

    if request.method == "POST":
        policy.policy_type = request.form.get("policy_type", policy.policy_type)
        policy.customer_id = int(request.form.get("customer_id", policy.customer_id))

        try:
            premium_value = float(request.form.get("premium", policy.premium))
            assert premium_value > 0
            policy.premium = premium_value
        except (ValueError, AssertionError):
            flash("Premium must be a positive number.", "danger")
            return render_template("policies/form.html", customers=customers, policy=policy)

        valid_from = parse_date(request.form.get("valid_from", ""))
        valid_to = parse_date(request.form.get("valid_to", ""))
        if not valid_from or not valid_to or valid_to < valid_from:
            flash("Please provide valid policy dates.", "danger")
            return render_template("policies/form.html", customers=customers, policy=policy)

        policy.valid_from = valid_from
        policy.valid_to = valid_to

        db.session.commit()
        flash("Policy updated.", "success")
        return redirect(url_for("policy.list_policies"))

    return render_template("policies/form.html", customers=customers, policy=policy)


@policy_bp.route("/<int:policy_id>/delete", methods=["POST"])
@role_required("admin")
def delete_policy(policy_id: int):
    policy = Policy.query.get_or_404(policy_id)
    db.session.delete(policy)
    db.session.commit()
    flash("Policy deleted.", "info")
    return redirect(url_for("policy.list_policies"))
