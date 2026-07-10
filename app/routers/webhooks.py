from fastapi import APIRouter

from app.core.logger import logger
from app.schemas.mpesa import StkCallbackRequest
from app.services.mpesa_service import MpesaService

router = APIRouter(
    prefix="/webhooks",
    tags=["Webhooks"],
)


@router.post("/mpesa/{realm_id}")
def mpesa_callback(
    realm_id: str,
    payload: StkCallbackRequest,
):

    try:
        return MpesaService.process_stk_callback(
            realm_id=realm_id,
            payload=payload,
        )
    except Exception as e:
        logger.exception("STK callback processing failed")
        return {
            "ResultCode": 1,
            "ResultDesc": str(e),
        }