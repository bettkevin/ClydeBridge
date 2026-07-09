from fastapi import APIRouter

from app.core.logger import logger
from app.schemas.mpesa_callback import MpesaCallbackRequest
from app.services.mpesa_callback_service import MpesaCallbackService

router = APIRouter(
    prefix="/mpesa",
    tags=["M-Pesa"],
)


@router.post("/confirmation")
def confirmation(
    realm_id: str,
    callback: MpesaCallbackRequest,
):

    logger.info(
        f"M-Pesa callback received: {callback.TransID}"
    )

    return MpesaCallbackService.process(
        realm_id=realm_id,
        callback=callback,
    )


@router.post("/validation")
def validation():

    logger.info("Validation request received")

    return {
        "ResultCode": 0,
        "ResultDesc": "Accepted",
    }