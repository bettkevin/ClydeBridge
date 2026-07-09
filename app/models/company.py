from datetime import datetime

from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Integer
from sqlalchemy import String

from app.database.db import Base


class Company(Base):

    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, index=True)

    company_name = Column(String, nullable=False)

    legal_name = Column(String)

    realm_id = Column(String, unique=True, nullable=False)

    email = Column(String)

    country = Column(String)

    timezone = Column(String)

    subscription = Column(String)

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )