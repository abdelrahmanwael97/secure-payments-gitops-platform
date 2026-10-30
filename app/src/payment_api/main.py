from uuid import uuid4

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(
    title="Secure Payments API",
    description="A simulated payments API for a DevOps GitOps platform",
    version="1.0.0",
)

# Temporary in-memory storage for our lab.
payments = {}


class PaymentRequest(BaseModel):
    amount: float = Field(gt=0)
    currency: str = Field(pattern=r"^[A-Z]{3}$")
    description: str = Field(min_length=1, max_length=200)


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.get("/ready")
def readiness():
    return {"status": "ready"}


@app.post("/payments", status_code=201)
def create_payment(payment: PaymentRequest):
    payment_id = str(uuid4())

    payment_record = {
        "payment_id": payment_id,
        "amount": payment.amount,
        "currency": payment.currency,
        "description": payment.description,
        "status": "simulated",
    }

    payments[payment_id] = payment_record

    return payment_record


@app.get("/payments/{payment_id}")
def get_payment(payment_id: str):
    payment = payments.get(payment_id)

    if payment is None:
        raise HTTPException(
            status_code=404,
            detail="Payment not found",
        )

    return payment
