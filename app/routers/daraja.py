from fastapi import APIRouter

from app.services.daraja_service import DarajaService

router = APIRouter(
    prefix="/daraja",
    tags=["Daraja"],
)


@router.get("/token")
def get_token():

    token = DarajaService.get_access_token()

    return {
        "access_token": token
    }


@router.post("/register")
def register_urls():

    return DarajaService.register_urls()