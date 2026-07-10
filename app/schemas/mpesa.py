from typing import Any, List, Optional

from pydantic import BaseModel, Field


# --------------------------------------------------
# Legacy / manual payment request (kept for /payments)
# --------------------------------------------------
class MpesaPaymentRequest(BaseModel):
    receipt: str = Field(...)
    invoice_number: str = Field(...)
    amount: float = Field(..., gt=0)
    phone: str = Field(...)


# --------------------------------------------------
# Safaricom STK Push callback payload
# --------------------------------------------------
class StkCallbackItem(BaseModel):
    Name: str
    Value: Optional[Any] = None


class StkCallbackMetadata(BaseModel):
    Item: List[StkCallbackItem] = []


class StkCallback(BaseModel):
    MerchantRequestID: str
    CheckoutRequestID: str
    ResultCode: int
    ResultDesc: str
    CallbackMetadata: Optional[StkCallbackMetadata] = None


class StkCallbackBody(BaseModel):
    stkCallback: StkCallback


class StkCallbackRequest(BaseModel):
    Body: StkCallbackBody

    def is_successful(self) -> bool:
        return self.Body.stkCallback.ResultCode == 0

    def get_metadata(self) -> dict:
        """Return CallbackMetadata items as a plain dict."""
        metadata = self.Body.stkCallback.CallbackMetadata
        if not metadata:
            return {}
        return {item.Name: item.Value for item in metadata.Item}
