from fastapi import FastAPI

from app.routers.auth import router as auth_router
from app.routers.customers import router as customer_router
from app.routers.invoices import router as invoice_router
from app.routers.payments import router as payment_router
from app.routers.webhooks import router as webhook_router
from app.routers.mpesa import router as mpesa_router
from app.routers.daraja import router as daraja_router

app = FastAPI(
    title="Clyde Bridge",
    version="1.0.0",
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

# Daraja
app.include_router(daraja_router)


@app.get("/")
def root():
    return {
        "application": "Clyde Bridge",
        "version": "1.0.0",
        "status": "running",
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
    }