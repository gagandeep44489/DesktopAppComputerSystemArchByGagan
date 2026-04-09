"""Policy model."""

from __future__ import annotations

from datetime import date, datetime

from app.extensions import db


class Policy(db.Model):
    """Insurance policy issued to customers."""

    id = db.Column(db.Integer, primary_key=True)
    policy_number = db.Column(db.String(50), nullable=False, unique=True, index=True)
    policy_type = db.Column(db.String(80), nullable=False)
    premium = db.Column(db.Float, nullable=False)
    valid_from = db.Column(db.Date, nullable=False)
    valid_to = db.Column(db.Date, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    customer_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    customer = db.relationship("User", back_populates="policies")

    claims = db.relationship("Claim", back_populates="policy", cascade="all, delete-orphan")

    @property
    def is_active(self) -> bool:
        today = date.today()
        return self.valid_from <= today <= self.valid_to
