"""Claim routes."""

from __future__ import annotations

import uuid

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from app.extensions import db
from app.models.claim import Claim
from app.models.notification import Notification
from app.models.policy import Policy
from app.utils import parse_date, role_required, save_uploaded_document


claim_bp = Blueprint("claim", __name__, url_prefix="/claims")


@claim_bp.route("/")
@login_required
def list_claims():
    search = request.args.get("search", "").strip()
    status = request.args.get("status", "").strip()
    page = request.args.get("page", default=1, type=int)

    query = Claim.query
    if not current_user.is_admin():
        query = query.filter_by(customer_id=current_user.id)

    if search:
        query = query.filter(Claim.claim_id.ilike(f"%{search}%"))
    if status:
        query = query.filter_by(status=status)

    claims = query.order_by(Claim.created_at.desc()).paginate(page=page, per_page=10)
    return render_template("claims/list.html", claims=claims, search=search, status=status)


@claim_bp.route("/new", methods=["GET", "POST"])
@role_required("customer")
def create_claim():
    policies = Policy.query.filter_by(customer_id=current_user.id).order_by(Policy.created_at.desc())

    if request.method == "POST":
        policy_id = request.form.get("policy_id", "")
        claim_amount = request.form.get("claim_amount", "")
        description = request.form.get("description", "").strip()
        incident_date = parse_date(request.form.get("incident_date", ""))

        policy = Policy.query.filter_by(id=policy_id, customer_id=current_user.id).first()
        if not policy:
            flash("Please choose a valid policy.", "danger")
            return render_template("claims/form.html", policies=policies)

        try:
            claim_amount_value = float(claim_amount)
            assert claim_amount_value > 0
        except (ValueError, AssertionError):
            flash("Claim amount must be positive.", "danger")
            return render_template("claims/form.html", policies=policies)

        if not incident_date:
            flash("Please provide a valid date in YYYY-MM-DD format.", "danger")
            return render_template("claims/form.html", policies=policies)

        document_name = save_uploaded_document(request.files.get("document"))

        claim = Claim(
            claim_id=f"CLM-{uuid.uuid4().hex[:8].upper()}",
            policy_id=policy.id,
            customer_id=current_user.id,
            claim_amount=claim_amount_value,
            description=description,
            incident_date=incident_date,
            document_filename=document_name,
        )

        db.session.add(claim)
        db.session.commit()
        flash("Claim submitted successfully.", "success")
        return redirect(url_for("claim.list_claims"))

    return render_template("claims/form.html", policies=policies)


@claim_bp.route("/<int:claim_id>/status", methods=["POST"])
@role_required("admin")
def update_status(claim_id: int):
    claim = Claim.query.get_or_404(claim_id)
    new_status = request.form.get("status", "Pending")

    if new_status not in {"Pending", "Approved", "Rejected"}:
        flash("Invalid status.", "danger")
        return redirect(url_for("claim.list_claims"))

    claim.status = new_status
    db.session.add(
        Notification(
            user_id=claim.customer_id,
            message=f"Your claim {claim.claim_id} status changed to {new_status}.",
        )
    )
    db.session.commit()
    flash("Claim status updated.", "success")
    return redirect(url_for("claim.list_claims"))
