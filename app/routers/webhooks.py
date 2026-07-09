from fastapi import APIRouter

from app.schemas.mpesa import MpesaPaymentRequest
from app.services.mpesa_service import MpesaService

router = APIRouter(
    prefix="/webhooks",
    tags=["Webhooks"],
)


@router.post("/mpesa")
def mpesa_callback(
    realm_id: str,
    payment: MpesaPaymentRequest,
):

    return MpesaService.process_payment(
        realm_id=realm_id,
        payment=payment,
    )