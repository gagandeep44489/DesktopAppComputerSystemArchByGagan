"""Claim model."""

from __future__ import annotations

from datetime import date, datetime

from app.extensions import db


class Claim(db.Model):
    """Insurance claim submitted by customers."""

    id = db.Column(db.Integer, primary_key=True)
    claim_id = db.Column(db.String(40), unique=True, nullable=False, index=True)
    claim_amount = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, nullable=False)
    incident_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(20), nullable=False, default="Pending")
    document_filename = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    policy_id = db.Column(db.Integer, db.ForeignKey("policy.id"), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    policy = db.relationship("Policy", back_populates="claims")
    customer = db.relationship("User", back_populates="claims")

    def approval_probability(self) -> float:
        """Simple heuristic to estimate approval chance."""

        score = 0.9
        if self.claim_amount > self.policy.premium * 12:
            score -= 0.25
        if not self.policy.is_active:
            score -= 0.35
        if (date.today() - self.incident_date).days > 90:
            score -= 0.15
        return max(0.05, min(score, 0.98))

    def fraud_risk_score(self) -> float:
        """Simple fraud-risk indicator (0 to 1)."""

        risk = 0.1
        if self.claim_amount > self.policy.premium * 18:
            risk += 0.35
        if self.status == "Rejected":
            risk += 0.2
        if len(self.description or "") < 25:
            risk += 0.2
        return min(risk, 0.95)
