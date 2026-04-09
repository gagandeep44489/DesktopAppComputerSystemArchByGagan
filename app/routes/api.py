"""REST API endpoints."""

from flask import Blueprint, jsonify
from flask_login import login_required

from app.models.claim import Claim
from app.models.policy import Policy
from app.models.user import User
from app.utils import role_required


api_bp = Blueprint("api", __name__)


@api_bp.get("/claims")
@login_required
def claims_api():
    query = Claim.query
    from flask_login import current_user

    if not current_user.is_admin():
        query = query.filter_by(customer_id=current_user.id)

    data = [
        {
            "claim_id": c.claim_id,
            "policy_id": c.policy_id,
            "customer_id": c.customer_id,
            "amount": c.claim_amount,
            "status": c.status,
            "approval_probability": c.approval_probability(),
            "fraud_risk_score": c.fraud_risk_score(),
        }
        for c in query.all()
    ]
    return jsonify(data)


@api_bp.get("/policies")
@login_required
def policies_api():
    query = Policy.query
    from flask_login import current_user

    if not current_user.is_admin():
        query = query.filter_by(customer_id=current_user.id)

    data = [
        {
            "id": p.id,
            "policy_number": p.policy_number,
            "policy_type": p.policy_type,
            "premium": p.premium,
            "valid_from": p.valid_from.isoformat(),
            "valid_to": p.valid_to.isoformat(),
            "customer_id": p.customer_id,
        }
        for p in query.all()
    ]
    return jsonify(data)


@api_bp.get("/users")
@role_required("admin")
def users_api():
    data = [{"id": u.id, "name": u.full_name, "email": u.email, "role": u.role} for u in User.query.all()]
    return jsonify(data)
