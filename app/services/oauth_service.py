import base64

import requests
from requests.exceptions import HTTPError, RequestException

from app.core.config import settings
from app.core.logger import logger


class OAuthService:

    @staticmethod
    def _headers():

        credentials = (
            f"{settings.QBO_CLIENT_ID}:"
            f"{settings.QBO_CLIENT_SECRET}"
        )

        encoded_credentials = base64.b64encode(
            credentials.encode("utf-8")
        ).decode("utf-8")

        return {
            "Authorization": f"Basic {encoded_credentials}",
            "Accept": "application/json",
            "Content-Type": "application/x-www-form-urlencoded",
        }

    @staticmethod
    def exchange_code(code: str) -> dict:
        """
        Exchange authorization code for tokens.
        """

        logger.info(
            "Exchanging authorization code for access token"
        )

        payload = {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": settings.QBO_REDIRECT_URI,
        }

        try:

            response = requests.post(
                settings.QBO_TOKEN_URL,
                headers=OAuthService._headers(),
                data=payload,
                timeout=30,
            )

            response.raise_for_status()

            logger.info(
                "OAuth token exchange successful"
            )

            return response.json()

        except HTTPError:

            logger.error(response.text)
            raise

        except RequestException as e:

            logger.exception(
                "Unable to connect to QuickBooks"
            )

            raise Exception(
                "Unable to connect to QuickBooks."
            ) from e

    @staticmethod
    def refresh_access_token(
        refresh_token: str,
    ) -> dict:
        """
        Refresh an expired QuickBooks access token.
        """

        logger.info(
            "Refreshing QuickBooks access token"
        )

        payload = {
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
        }

        try:

            response = requests.post(
                settings.QBO_TOKEN_URL,
                headers=OAuthService._headers(),
                data=payload,
                timeout=30,
            )

            response.raise_for_status()

            logger.info(
                "Access token refreshed successfully"
            )

            return response.json()

        except HTTPError:

            logger.error(response.text)
            raise

        except RequestException as e:

            logger.exception(
                "Unable to refresh access token"
            )

            raise Exception(
                "Unable to connect to QuickBooks."
            ) from e