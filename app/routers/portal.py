from fastapi import APIRouter

router = APIRouter(
    prefix="/pay",
    tags=["Payment Portal"]
)


@router.get("/{token}")
async def payment_page(token: str):
    return {
        "message": "Welcome to ClydeBridge Payment Portal",
        "token": token,
        "status": "ready"
    }