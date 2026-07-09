from fastapi import FastAPI

from app.core.version import APP_NAME, VERSION
from app.routers.auth import router as auth_router
from app.routers.customers import router as customer_router
from app.routers.invoices import router as invoice_router
from app.routers.payments import router as payment_router
from app.routers.webhooks import router as webhook_router
from app.routers.mpesa import router as mpesa_router
from app.routers.daraja import router as daraja_router

app = FastAPI(
    title=APP_NAME,
    version=VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
)

# Authentication
app.include_router(auth_router)

# QuickBooks
app.include_router(customer_router)
app.include_router(invoice_router)
app.include_router(payment_router)

# Internal Webhooks
app.include_router(webhook_router)

# M-Pesa
app.include_router(mpesa_router)
app.include_router(daraja_router)


@app.get("/", tags=["System"])
def root():
    return {
        "application": APP_NAME,
        "version": VERSION,
        "status": "running",
    }


@app.get("/health", tags=["System"])
def health():
    return {
        "status": "healthy",
        "application": APP_NAME,
        "version": VERSION,
    }