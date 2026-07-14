import secrets
from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from app.core.logger import logger
from app.database.db import SessionLocal
from app.models.payment_session import PaymentSession


class PaymentSessionService:

    @staticmethod
    def create_session(
        invoice_id: str,
        invoice_number: str,
        customer_name: str,
        amount: float,
        currency: str = "KES",
        customer_email: str = None,
        phone_number: str = None,
    ) -> PaymentSession:

        db: Session = SessionLocal()

        try:
            session = PaymentSession(
                token=secrets.token_urlsafe(32),
                invoice_id=invoice_id,
                invoice_number=invoice_number,
                customer_name=customer_name,
                customer_email=customer_email,
                phone_number=phone_number,
                amount=amount,
                currency=currency,
                status="PENDING",
                expires_at=datetime.utcnow() + timedelta(hours=24),
            )

            db.add(session)
            db.commit()
            db.refresh(session)

            logger.info(
                f"Payment session created | Invoice: {invoice_number} | Token: {session.token[:8]}..."
            )

            db.expunge(session)
            return session

        finally:
            db.close()

    @staticmethod
    def get_by_token(token: str) -> PaymentSession | None:

        db: Session = SessionLocal()

        try:
            session = (
                db.query(PaymentSession)
                .filter(PaymentSession.token == token)
                .first()
            )

            if not session:
                return None

            if session.expires_at and session.expires_at < datetime.utcnow():
                logger.warning(f"Payment session expired | Token: {token[:8]}...")
                return None

            db.expunge(session)
            return session

        finally:
            db.close()

    @staticmethod
    def update_status(
        token: str,
        status: str,
        receipt_number: str = None,
        checkout_request_id: str = None,
        merchant_request_id: str = None,
    ) -> PaymentSession | None:

        db: Session = SessionLocal()

        try:
            session = (
                db.query(PaymentSession)
                .filter(PaymentSession.token == token)
                .first()
            )

            if not session:
                return None

            session.status = status

            if receipt_number:
                session.receipt_number = receipt_number
            if checkout_request_id:
                session.checkout_request_id = checkout_request_id
            if merchant_request_id:
                session.merchant_request_id = merchant_request_id

            db.commit()
            db.refresh(session)

            logger.info(
                f"Payment session updated | Token: {token[:8]}... | Status: {status}"
            )

            db.expunge(session)
            return session

        finally:
            db.close()

    @staticmethod
    def get_by_checkout_request_id(checkout_request_id: str) -> PaymentSession | None:

        db: Session = SessionLocal()

        try:
            session = (
                db.query(PaymentSession)
                .filter(PaymentSession.checkout_request_id == checkout_request_id)
                .first()
            )

            if session:
                db.expunge(session)
            return session

        finally:
            db.close()
