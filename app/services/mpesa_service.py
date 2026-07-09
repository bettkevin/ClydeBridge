from app.schemas.mpesa import MpesaPaymentRequest
from app.services.payment_service import PaymentService


class MpesaService:

    @staticmethod
    def process_payment(
        realm_id: str,
        payment: MpesaPaymentRequest,
    ):

        return PaymentService.create_payment(
            realm_id=realm_id,
            invoice_number=payment.invoice_number,
            amount=payment.amount,
        )