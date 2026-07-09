from app.services.invoice_service import InvoiceService
from app.services.quickbooks_client import QuickBooksClient


class PaymentService:

    @staticmethod
    def create_payment(
        realm_id: str,
        invoice_number: str,
        amount: float,
    ):

        invoice = InvoiceService.find_invoice_by_number(
            realm_id=realm_id,
            invoice_number=invoice_number,
        )

        if not invoice:
            raise Exception("Invoice not found.")

        payload = {
            "CustomerRef": {
                "value": invoice["CustomerRef"]["value"]
            },
            "TotalAmt": amount,
            "Line": [
                {
                    "Amount": amount,
                    "LinkedTxn": [
                        {
                            "TxnId": invoice["Id"],
                            "TxnType": "Invoice"
                        }
                    ]
                }
            ]
        }

        return QuickBooksClient.post(
            realm_id=realm_id,
            endpoint="payment",
            payload=payload,
        )
