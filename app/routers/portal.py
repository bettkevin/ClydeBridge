from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.services.invoice_service import InvoiceService

router = APIRouter(
    prefix="/pay",
    tags=["Payment Portal"]
)

templates = Jinja2Templates(directory="app/templates")


@router.get("/{realm_id}/{invoice_number}", response_class=HTMLResponse)
async def payment_page(
    request: Request,
    realm_id: str,
    invoice_number: str,
):

    invoice = InvoiceService.find_invoice_by_number(
        realm_id,
        invoice_number,
    )

    if not invoice:
        raise HTTPException(
            status_code=404,
            detail="Invoice not found."
        )

    customer = invoice.get("CustomerRef", {}).get("name", "")

    balance = invoice.get("Balance", 0)

    currency = invoice.get(
        "CurrencyRef",
        {}
    ).get(
        "value",
        "KES"
    )

    return templates.TemplateResponse(
        request,
        "payment.html",
        {
            "request": request,
            "company": "ClydeBridge",
            "invoice_number": invoice.get("DocNumber"),
            "customer": customer,
            "amount": balance,
            "currency": currency,
            "realm_id": realm_id,
        }
    )