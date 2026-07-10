from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from app.core.logger import logger
from app.database.db import SessionLocal
from app.models.oauth_token import OAuthToken
from app.services.oauth_service import OAuthService


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

            db.expunge(token)
            return token

        finally:

            db.close()

    @staticmethod
    def get_token(
        company_id: int,
    ) -> OAuthToken | None:

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
                return None

            if (
                token.expires_at
                and token.expires_at <= datetime.utcnow()
            ):

                logger.info(
                    "QuickBooks access token expired. Refreshing..."
                )

                refreshed = OAuthService.refresh_access_token(
                    token.refresh_token
                )

                token.access_token = refreshed["access_token"]
                token.refresh_token = refreshed["refresh_token"]

                token.expires_at = (
                    datetime.utcnow()
                    + timedelta(
                        seconds=refreshed.get(
                            "expires_in",
                            3600,
                        )
                    )
                )

                db.commit()
                db.refresh(token)

                logger.info(
                    "QuickBooks token refreshed successfully."
                )

            db.expunge(token)
            return token

        finally:

            db.close()

    @staticmethod
    def update_tokens(
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

            if not token:
                raise Exception(
                    "OAuth token not found."
                )

            token.access_token = access_token
            token.refresh_token = refresh_token
            token.expires_at = expires_at

            db.commit()
            db.refresh(token)

            logger.info(
                "OAuth tokens refreshed successfully"
            )

            db.expunge(token)
            return token

        finally:

            db.close()