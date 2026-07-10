from fastapi import APIRouter

from app.core.logger import logger
from app.schemas.mpesa_callback import MpesaCallbackRequest
from app.services.mpesa_callback_service import MpesaCallbackService

router = APIRouter(
    prefix="/mpesa",
    tags=["M-Pesa"],
)


@router.post("/confirmation/{realm_id}")
def confirmation(
    realm_id: str,
    callback: MpesaCallbackRequest,
):

    logger.info(
        f"M-Pesa callback received: {callback.TransID}"
    )

    try:
        return MpesaCallbackService.process(
            realm_id=realm_id,
            callback=callback,
        )
    except Exception as e:
        logger.exception("M-Pesa confirmation processing failed")
        return {
            "ResultCode": 1,
            "ResultDesc": str(e),
        }


@router.post("/validation")
def validation():

    logger.info("Validation request received")

    return {
        "ResultCode": 0,
        "ResultDesc": "Accepted",
    }