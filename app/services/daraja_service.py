import base64
import requests

from app.core.config import settings


class DarajaService:

    BASE_URL = (
        "https://sandbox.safaricom.co.ke"
        if settings.MPESA_ENVIRONMENT == "sandbox"
        else "https://api.safaricom.co.ke"
    )

    @staticmethod
    def get_access_token():

        credentials = (
            f"{settings.MPESA_CONSUMER_KEY}:"
            f"{settings.MPESA_CONSUMER_SECRET}"
        )

        encoded = base64.b64encode(
            credentials.encode()
        ).decode()

        headers = {
            "Authorization": f"Basic {encoded}"
        }

        response = requests.get(
            f"{DarajaService.BASE_URL}/oauth/v1/generate?grant_type=client_credentials",
            headers=headers,
            timeout=30,
        )

        response.raise_for_status()

        return response.json()["access_token"]

    @staticmethod
    def register_urls():

        token = DarajaService.get_access_token()

        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }

        payload = {
            "ShortCode": settings.MPESA_SHORTCODE,
            "ResponseType": "Completed",
            "ConfirmationURL": settings.MPESA_CONFIRMATION_URL,
            "ValidationURL": settings.MPESA_VALIDATION_URL,
        }

        response = requests.post(
            f"{DarajaService.BASE_URL}/mpesa/c2b/v1/registerurl",
            json=payload,
            headers=headers,
            timeout=30,
        )

        response.raise_for_status()

        return response.json()