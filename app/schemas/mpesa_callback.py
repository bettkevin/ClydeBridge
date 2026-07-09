from pydantic import BaseModel


class MpesaCallbackRequest(BaseModel):

    TransactionType: str

    TransID: str

    TransTime: str

    TransAmount: float

    BusinessShortCode: str

    BillRefNumber: str

    InvoiceNumber: str | None = None

    OrgAccountBalance: str | None = None

    ThirdPartyTransID: str | None = None

    MSISDN: str

    FirstName: str

    MiddleName: str | None = None

    LastName: str | None = None