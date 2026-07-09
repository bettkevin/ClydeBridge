import requests
from requests.exceptions import HTTPError, RequestException

from app.core.config import settings
from app.core.logger import logger


class QuickBooksService:

    @staticmethod
    def get_company_info(
        access_token: str,
        realm_id: str,
    ) -> dict:
        """
        Retrieve Company Information from QuickBooks.
        """

        url = (
            f"{settings.qbo_base_url}"
            f"/v3/company/{realm_id}/companyinfo/{realm_id}"
        )

        headers = {
            "Authorization": f"Bearer {access_token}",
            "Accept": "application/json",
        }

        try:

            logger.info("Retrieving company information")

            response = requests.get(
                url,
                headers=headers,
                timeout=30,
            )

            response.raise_for_status()

            logger.info("Company information retrieved successfully")

            return response.json()

        except HTTPError:

            logger.error(response.text)
            raise

        except RequestException as e:

            logger.exception("Unable to connect to QuickBooks")

            raise Exception(
                "Unable to connect to QuickBooks."
            ) from e