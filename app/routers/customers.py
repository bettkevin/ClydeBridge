from fastapi import APIRouter, HTTPException

from app.core.logger import logger
from app.services.customer_service import CustomerService

router = APIRouter(
    prefix="/customers",
    tags=["Customers"],
)


@router.get("/{realm_id}")
def get_customers(realm_id: str):
    """
    Retrieve customers from QuickBooks.
    """

    try:

        logger.info(
            f"Retrieving customers for realm {realm_id}"
        )

        customers = CustomerService.get_customers(
            realm_id
        )

        return customers

    except Exception as e:

        logger.exception(
            "Unable to retrieve customers"
        )

        raise HTTPException(status_code=500, detail=str(e))