from datetime import datetime

from sqlalchemy.orm import Session

from app.core.logger import logger
from app.database.db import SessionLocal
from app.models.oauth_token import OAuthToken


class TokenService:

    @staticmethod
    def save_token(
        company_id: int,
        access_token: str,
        refresh_token: str,
        expires_at: datetime | None,
    ) -> OAuthToken:

        db: Session = SessionLocal()

        try:

            token = (
                db.query(OAuthToken)
                .filter(
                    OAuthToken.company_id == company_id
                )
                .first()
            )

            if token:

                logger.info(
                    "Updating existing OAuth token"
                )

                token.access_token = access_token
                token.refresh_token = refresh_token
                token.expires_at = expires_at

            else:

                logger.info(
                    "Creating new OAuth token"
                )

                token = OAuthToken(
                    company_id=company_id,
                    access_token=access_token,
                    refresh_token=refresh_token,
                    expires_at=expires_at,
                )

                db.add(token)

            db.commit()
            db.refresh(token)

            logger.info(
                "OAuth token saved successfully"
            )

            return token

        finally:

            db.close()

    @staticmethod
    def get_token(
        company_id: int,
    ) -> OAuthToken | None:

        db: Session = SessionLocal()

        try:

            return (
                db.query(OAuthToken)
                .filter(
                    OAuthToken.company_id == company_id
                )
                .first()
            )

        finally:

            db.close()

    @staticmethod
    def update_tokens(
        company_id: int,
        access_token: str,
        refresh_token: str,
    ):

        db: Session = SessionLocal()

        try:

            token = (
                db.query(OAuthToken)
                .filter(
                    OAuthToken.company_id == company_id
                )
                .first()
            )

            if not token:
                raise Exception(
                    "OAuth token not found."
                )

            token.access_token = access_token
            token.refresh_token = refresh_token

            db.commit()

            logger.info(
                "OAuth tokens refreshed successfully"
            )

        finally:

            db.close()