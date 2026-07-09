from pydantic import BaseModel, Field


class MpesaPaymentRequest(BaseModel):
    receipt: str = Field(...)

    invoice_number: str = Field(...)

    amount: float = Field(..., gt=0)

    phone: str = Field(...)