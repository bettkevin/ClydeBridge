import os
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.version import APP_NAME, VERSION
from app.database.db import Base, engine

# Routers
from app.routers.auth import router as auth_router
from app.routers.customers import router as customer_router
from app.routers.invoices import router as invoice_router
from app.routers.payments import router as payment_router
from app.routers.webhooks import router as webhook_router
from app.routers.mpesa import router as mpesa_router
from app.routers.daraja import router as daraja_router
from app.routers.portal import router as portal_router

# Import models so metadata is populated before create_all
from app.models import company, oauth_token  # noqa: F401


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create tables on startup if they don't exist
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title=APP_NAME,
    version=VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# Authentication
app.include_router(auth_router)

# QuickBooks
app.include_router(customer_router)
app.include_router(invoice_router)
app.include_router(payment_router)

# Payment Portal
app.include_router(portal_router)

# Internal Webhooks
app.include_router(webhook_router)

# M-Pesa
app.include_router(mpesa_router)
app.include_router(daraja_router)


@app.get("/", tags=["System"])
async def root():
    return {
        "application": APP_NAME,
        "version": VERSION,
        "status": "running",
        "environment": os.getenv("ENVIRONMENT", "production"),
    }


@app.get("/health", tags=["System"])
async def health():
    return {
        "status": "healthy",
        "application": APP_NAME,
        "version": VERSION,
    }


@app.get("/version", tags=["System"])
async def version():
    return {
        "application": APP_NAME,
        "version": VERSION,
    }


@app.get("/routes", tags=["System"])
async def routes():
    from fastapi.routing import APIRoute

    def collect(router):
        result = []
        for r in router.routes:
            if isinstance(r, APIRoute):
                result.append({
                    "path": r.path,
                    "methods": sorted(list(r.methods)),
                    "name": r.name,
                })
            orig = getattr(r, "original_router", None)
            if orig:
                result.extend(collect(orig))
        return result

    return sorted(collect(app.router), key=lambda r: r["path"])
