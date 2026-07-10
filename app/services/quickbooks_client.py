import requests
from requests.exceptions import HTTPError, RequestException

from app.core.config import settings
from app.core.logger import logger
from app.services.company_service import CompanyService
from app.services.token_service import TokenService


class QuickBooksClient:

    @staticmethod
    def get_company(realm_id: str):

        company = CompanyService.get_by_realm_id(
            realm_id
        )

        if not company:
            raise Exception("Company not found.")

        return company

    @staticmethod
    def get_token(realm_id: str):

        company = QuickBooksClient.get_company(
            realm_id
        )

        token = TokenService.get_token(
            company.id
        )

        if not token:
            raise Exception(
                "OAuth token not found."
            )

        return token

    @staticmethod
    def post_query(
        realm_id: str,
        query: str,
    ):

        token = QuickBooksClient.get_token(
            realm_id
        )

        url = (
            f"{settings.qbo_base_url}"
            f"/v3/company/{realm_id}/query"
        )

        headers = {
            "Authorization": f"Bearer {token.access_token}",
            "Accept": "application/json",
            "Content-Type": "text/plain",
        }

        try:

            logger.info(f"QBO Query: {query}")

            response = requests.post(
                url,
                headers=headers,
                data=query,
                timeout=30,
            )

            if response.status_code == 401:
                logger.error(
                    "QuickBooks returned 401 Unauthorized."
                )
                logger.error(response.text)
                raise Exception(
                    "QuickBooks access token has expired."
                )

            if response.status_code >= 400:
                logger.error(response.text)
                raise Exception(response.text)

            return response.json()

        except RequestException as e:

            logger.exception(
                "QuickBooks query failed"
            )

            raise Exception(
                "Unable to connect to QuickBooks."
            ) from e

    @staticmethod
    def post(
        realm_id: str,
        endpoint: str,
        payload: dict,
    ):

        token = QuickBooksClient.get_token(
            realm_id
        )

        url = (
            f"{settings.qbo_base_url}"
            f"/v3/company/{realm_id}/{endpoint}"
        )

        headers = {
            "Authorization": f"Bearer {token.access_token}",
            "Accept": "application/json",
            "Content-Type": "application/json",
        }

        try:

            logger.info(
                f"POST {endpoint} to QuickBooks"
            )

            response = requests.post(
                url,
                headers=headers,
                json=payload,
                timeout=30,
            )

            if response.status_code == 401:
                logger.error(
                    "QuickBooks returned 401 Unauthorized."
                )
                logger.error(response.text)
                raise Exception(
                    "QuickBooks access token has expired."
                )

            if response.status_code >= 400:
                logger.error(response.text)
                raise Exception(response.text)

            return response.json()

        except RequestException as e:

            logger.exception(
                "QuickBooks POST failed"
            )

            raise Exception(
                "Unable to connect to QuickBooks."
            ) from e