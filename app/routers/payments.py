from fastapi import APIRouter, HTTPException

from app.core.logger import logger
from app.schemas.payment import PaymentRequest
from app.services.payment_service import PaymentService

router = APIRouter(
    prefix="/payments",
    tags=["Payments"],
)


@router.post("/")
def create_payment(
    payment: PaymentRequest,
):

    try:

        logger.info(
            f"Creating payment for invoice "
            f"{payment.invoice_number}"
        )

        return PaymentService.create_payment(
            realm_id=payment.realm_id,
            invoice_number=payment.invoice_number,
            amount=payment.amount,
        )

    except Exception as e:

        logger.exception(
            "Payment creation failed"
        )

        raise HTTPException(status_code=500, detail=str(e))