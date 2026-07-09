from app.database.db import Base
from app.database.db import engine

from app.models.company import Company
from app.models.oauth_token import OAuthToken

Base.metadata.create_all(bind=engine)

print("Database created successfully.")