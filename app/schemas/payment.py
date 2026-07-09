from pydantic import BaseModel, Field


class PaymentRequest(BaseModel):

    realm_id: str = Field(
        ...,
        description="QuickBooks Realm ID"
    )

    invoice_number: str = Field(
        ...,
        description="Invoice Number"
    )

    amount: float = Field(
        ...,
        gt=0,
        description="Payment Amount"
    )