from app.core.logger import logger
from app.schemas.mpesa import StkCallbackRequest
from app.services.payment_service import PaymentService


class MpesaService:

    @staticmethod
    def process_stk_callback(
        realm_id: str,
        payload: StkCallbackRequest,
    ):
        callback = payload.Body.stkCallback

        logger.info("========== STK CALLBACK ==========")
        logger.info(f"ResultCode : {callback.ResultCode}")
        logger.info(f"ResultDesc : {callback.ResultDesc}")

        if not payload.is_successful():
            logger.warning(
                f"STK Push failed: {callback.ResultDesc}"
            )
            return {
                "ResultCode": callback.ResultCode,
                "ResultDesc": callback.ResultDesc,
            }

        meta = payload.get_metadata()

        receipt = meta.get("MpesaReceiptNumber")
        amount = meta.get("Amount")
        invoice_number = meta.get("AccountReference")

        logger.info(f"Receipt  : {receipt}")
        logger.info(f"Amount   : {amount}")
        logger.info(f"Invoice  : {invoice_number}")
        logger.info("==================================")

        if not invoice_number:
            logger.error(
                "AccountReference missing from STK callback metadata"
            )
            return {
                "ResultCode": 1,
                "ResultDesc": "Missing invoice reference.",
            }

        result = PaymentService.create_payment(
            realm_id=realm_id,
            invoice_number=invoice_number,
            amount=float(amount),
        )

        logger.info("Payment posted to QuickBooks")

        return {
            "ResultCode": 0,
            "ResultDesc": "Accepted",
            "QuickBooks": result,
        }
