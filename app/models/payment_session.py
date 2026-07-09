from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime, timedelta
import secrets

from app.database.db import Base


class PaymentSession(Base):
    __tablename__ = "payment_sessions"

    id = Column(Integer, primary_key=True, index=True)

    token = Column(
        String,
        unique=True,
        nullable=False,
        default=lambda: secrets.token_urlsafe(32)
    )

    invoice_id = Column(String, nullable=False)

    invoice_number = Column(String)

    customer_name = Column(String)

    customer_email = Column(String)

    phone_number = Column(String)

    amount = Column(Float)

    currency = Column(String, default="KES")

    status = Column(String, default="PENDING")

    receipt_number = Column(String)

    checkout_request_id = Column(String)

    merchant_request_id = Column(String)

    created_at = Column(DateTime, default=datetime.utcnow)

    expires_at = Column(
        DateTime,
        default=lambda: datetime.utcnow() + timedelta(hours=24)
    )