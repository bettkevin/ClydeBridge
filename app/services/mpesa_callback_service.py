from app.core.logger import logger
from app.schemas.mpesa_callback import MpesaCallbackRequest
from app.services.payment_service import PaymentService


class MpesaCallbackService:

    @staticmethod
    def process(
        realm_id: str,
        callback: MpesaCallbackRequest,
    ):

        logger.info("========== M-PESA PAYMENT ==========")
        logger.info(f"Receipt: {callback.TransID}")
        logger.info(f"Invoice: {callback.BillRefNumber}")
        logger.info(f"Amount: {callback.TransAmount}")
        logger.info(f"Phone: {callback.MSISDN}")

        result = PaymentService.create_payment(
            realm_id=realm_id,
            invoice_number=callback.BillRefNumber,
            amount=float(callback.TransAmount),
        )

        return {
            "ResultCode": 0,
            "ResultDesc": "Accepted",
            "QuickBooks": result,
        }