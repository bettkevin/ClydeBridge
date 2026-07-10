from fastapi import APIRouter, HTTPException

from app.core.logger import logger
from app.services.invoice_service import InvoiceService

router = APIRouter(
    prefix="/invoices",
    tags=["Invoices"],
)


@router.get("/{realm_id}")
def get_invoices(realm_id: str):

    try:

        logger.info(
            f"Retrieving invoices for {realm_id}"
        )

        return InvoiceService.get_invoices(
            realm_id
        )

    except Exception as e:

        logger.exception(
            "Unable to retrieve invoices"
        )

        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{realm_id}/{invoice_number}")
def get_invoice(
    realm_id: str,
    invoice_number: str,
):

    try:

        invoice = InvoiceService.find_invoice_by_number(
            realm_id,
            invoice_number,
        )

        if not invoice:
            raise HTTPException(
                status_code=404,
                detail="Invoice not found.",
            )

        return invoice

    except HTTPException:
        raise

    except Exception as e:

        logger.exception(
            "Unable to retrieve invoice"
        )

        raise HTTPException(status_code=500, detail=str(e))