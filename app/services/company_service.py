from sqlalchemy.orm import Session

from app.core.logger import logger
from app.database.db import SessionLocal
from app.models.company import Company


class CompanyService:

    @staticmethod
    def get_by_realm_id(realm_id: str):
        db: Session = SessionLocal()

        try:
            return (
                db.query(Company)
                .filter(Company.realm_id == realm_id)
                .first()
            )

        finally:
            db.close()

    @staticmethod
    def create_company(
        company_info: dict,
        realm_id: str,
    ):
        db: Session = SessionLocal()

        try:

            info = company_info["CompanyInfo"]

            company = (
                db.query(Company)
                .filter(Company.realm_id == realm_id)
                .first()
            )

            if company:
                logger.info("Company already exists")
                return company

            subscription = None

            for item in info.get("NameValue", []):
                if item.get("Name") == "OfferingSku":
                    subscription = item.get("Value")

            company = Company(
                company_name=info.get("CompanyName"),
                legal_name=info.get("LegalName"),
                realm_id=realm_id,
                email=info.get("Email", {}).get("Address"),
                country=info.get("Country"),
                timezone=info.get("DefaultTimeZone"),
                subscription=subscription,
            )

            db.add(company)
            db.commit()
            db.refresh(company)

            logger.info("Company saved successfully")

            return company

        finally:
            db.close()