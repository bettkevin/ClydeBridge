from fastapi import APIRouter, Request, HTTPException, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.core.logger import logger
from app.services.invoice_service import InvoiceService
from app.services.daraja_service import DarajaService

router = APIRouter(
    prefix="/pay",
    tags=["Payment Portal"],
)

templates = Jinja2Templates(directory="app/templates")


@router.get("/{realm_id}/{invoice_number}", response_class=HTMLResponse)
async def payment_page(
    request: Request,
    realm_id: str,
    invoice_number: str,
):

    try:
        invoice = InvoiceService.find_invoice_by_number(
            realm_id,
            invoice_number,
        )
    except Exception as e:
        logger.exception("Failed to load invoice for payment page")
        raise HTTPException(status_code=404, detail=str(e))

    if not invoice:
        raise HTTPException(
            status_code=404,
            detail="Invoice not found.",
        )

    customer = invoice.get(
        "CustomerRef",
        {},
    ).get(
        "name",
        "",
    )

    balance = invoice.get(
        "Balance",
        0,
    )

    currency = invoice.get(
        "CurrencyRef",
        {},
    ).get(
        "value",
        "KES",
    )

    return templates.TemplateResponse(
        request,
        "payment.html",
        {
            "request": request,
            "company": "ClydeBridge",
            "realm_id": realm_id,
            "invoice_number": invoice.get("DocNumber"),
            "customer": customer,
            "amount": balance,
            "currency": currency,
        },
    )


@router.post("/{realm_id}/{invoice_number}", response_class=HTMLResponse)
async def initiate_payment(
    request: Request,
    realm_id: str,
    invoice_number: str,
    phone: str = Form(...),
    amount: float = Form(...),
):

    invoice = InvoiceService.find_invoice_by_number(
        realm_id,
        invoice_number,
    )

    if not invoice:
        raise HTTPException(
            status_code=404,
            detail="Invoice not found.",
        )

    try:

        logger.info(
            f"Initiating STK Push | Invoice={invoice_number} | Phone={phone} | Amount={amount}"
        )

        response = DarajaService.stk_push(
            phone=phone,
            amount=amount,
            account_reference=invoice_number,
            description=f"Invoice {invoice_number}",
        )

        logger.info(f"Daraja Response: {response}")

        return templates.TemplateResponse(
            request,
            "pending.html",
            {
                "request": request,
                "invoice_number": invoice_number,
                "phone": phone,
                "amount": amount,
            },
        )

    except Exception as e:

        logger.exception("STK Push failed")

        raise HTTPException(
            status_code=500,
            detail=str(e),
        )