import base64
from datetime import datetime

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
    def generate_password():

        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

        password = base64.b64encode(
            (
                settings.MPESA_SHORTCODE +
                settings.MPESA_PASSKEY +
                timestamp
            ).encode()
        ).decode()

        return password, timestamp

    @staticmethod
    def stk_push(
        phone: str,
        amount: float,
        account_reference: str,
        description: str,
    ):

        token = DarajaService.get_access_token()

        password, timestamp = DarajaService.generate_password()

        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }

        payload = {
            "BusinessShortCode": settings.MPESA_SHORTCODE,
            "Password": password,
            "Timestamp": timestamp,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": int(amount),
            "PartyA": phone,
            "PartyB": settings.MPESA_SHORTCODE,
            "PhoneNumber": phone,
            "CallBackURL": settings.MPESA_CALLBACK_URL,
            "AccountReference": account_reference,
            "TransactionDesc": description,
        }

        response = requests.post(
            f"{DarajaService.BASE_URL}/mpesa/stkpush/v1/processrequest",
            json=payload,
            headers=headers,
            timeout=30,
        )

        response.raise_for_status()

        return response.json()

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