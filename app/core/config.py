import os
from dotenv import load_dotenv

load_dotenv()


class Settings:

    # ----------------------------------
    # Application
    # ----------------------------------
    APP_NAME = os.getenv("APP_NAME", "Clyde Bridge")
    ENVIRONMENT = os.getenv("ENVIRONMENT", "sandbox")

    # ----------------------------------
    # QuickBooks
    # ----------------------------------
    QBO_CLIENT_ID = os.getenv("QBO_CLIENT_ID")
    QBO_CLIENT_SECRET = os.getenv("QBO_CLIENT_SECRET")
    QBO_REDIRECT_URI = os.getenv("QBO_REDIRECT_URI")

    QBO_AUTH_URL = "https://appcenter.intuit.com/connect/oauth2"
    QBO_TOKEN_URL = (
        "https://oauth.platform.intuit.com/oauth2/v1/tokens/bearer"
    )

    QBO_API_BASE_URL = (
        "https://sandbox-quickbooks.api.intuit.com"
    )

    QBO_PRODUCTION_API_BASE_URL = (
        "https://quickbooks.api.intuit.com"
    )

    @property
    def qbo_base_url(self):
        if self.ENVIRONMENT.lower() == "production":
            return self.QBO_PRODUCTION_API_BASE_URL
        return self.QBO_API_BASE_URL

    # ----------------------------------
    # Safaricom Daraja
    # ----------------------------------
    MPESA_ENVIRONMENT = os.getenv(
        "MPESA_ENVIRONMENT",
        "sandbox"
    )

    MPESA_CONSUMER_KEY = os.getenv(
        "MPESA_CONSUMER_KEY"
    )

    MPESA_CONSUMER_SECRET = os.getenv(
        "MPESA_CONSUMER_SECRET"
    )

    MPESA_SHORTCODE = os.getenv(
        "MPESA_SHORTCODE"
    )

    MPESA_PASSKEY = os.getenv("MPESA_PASSKEY")

    MPESA_CALLBACK_URL = os.getenv("MPESA_CALLBACK_URL")

    MPESA_CONFIRMATION_URL = os.getenv(
        "MPESA_CONFIRMATION_URL"
    )

    MPESA_VALIDATION_URL = os.getenv(
        "MPESA_VALIDATION_URL"
    )

    @property
    def mpesa_base_url(self):
        if self.MPESA_ENVIRONMENT.lower() == "production":
            return "https://api.safaricom.co.ke"

        return "https://sandbox.safaricom.co.ke"


settings = Settings()