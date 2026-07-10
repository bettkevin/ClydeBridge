import urllib.parse
from datetime import datetime, timedelta

from fastapi import APIRouter, HTTPException
from fastapi.responses import RedirectResponse

from app.core.config import settings
from app.core.logger import logger
from app.services.company_service import CompanyService
from app.services.oauth_service import OAuthService
from app.services.quickbooks_service import QuickBooksService
from app.services.token_service import TokenService

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.get("/login")
def login():
    """
    Redirect the user to the QuickBooks OAuth page.
    """

    auth_url = (
        f"{settings.QBO_AUTH_URL}"
        f"?client_id={settings.QBO_CLIENT_ID}"
        "&response_type=code"
        "&scope=com.intuit.quickbooks.accounting"
        f"&redirect_uri={urllib.parse.quote(settings.QBO_REDIRECT_URI, safe='')}"
        "&state=clydebridge"
    )

    logger.info("Redirecting user to QuickBooks")

    return RedirectResponse(url=auth_url)


@router.get("/callback")
def callback(
    code: str,
    realmId: str,
    state: str | None = None,
):
    """
    Handle the QuickBooks OAuth callback.
    """

    try:

        logger.info("========== STARTING OAUTH CALLBACK ==========")

        # Exchange authorization code
        tokens = OAuthService.exchange_code(code)

        logger.info("========== TOKENS RECEIVED ==========")
        logger.info(tokens)
        logger.info("=====================================")

        access_token = tokens["access_token"]

        # Retrieve Company Information
        company_info = QuickBooksService.get_company_info(
            access_token=access_token,
            realm_id=realmId,
        )

        logger.info("Company information retrieved successfully")

        # Save Company
        company = CompanyService.create_company(
            company_info=company_info,
            realm_id=realmId,
        )

        logger.info(
            f"Company ID: {company.id} | Realm ID: {company.realm_id}"
        )

        # Calculate expiry
        expires_at = datetime.utcnow() + timedelta(
            seconds=tokens.get("expires_in", 3600)
        )

        logger.info(f"Calculated expires_at: {expires_at}")

        # Save Tokens
        token = TokenService.save_token(
            company_id=company.id,
            access_token=tokens["access_token"],
            refresh_token=tokens["refresh_token"],
            expires_at=expires_at,
        )

        logger.info("========== TOKEN SAVED ==========")
        logger.info(f"Database ID      : {token.id}")
        logger.info(f"Company ID       : {token.company_id}")
        logger.info(f"Expires At       : {token.expires_at}")
        logger.info("=================================")

        logger.info("QuickBooks connection saved successfully")

        return {
            "status": "success",
            "message": "QuickBooks company connected successfully.",
            "company": {
                "id": company.id,
                "name": company.company_name,
                "realm_id": company.realm_id,
                "country": company.country,
                "email": company.email,
            },
        }

    except Exception as e:

        logger.exception("QuickBooks connection failed")

        raise HTTPException(status_code=500, detail=str(e))