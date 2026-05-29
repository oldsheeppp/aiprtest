from typing import Literal

from fastapi import HTTPException, status
from pydantic import BaseModel, Field, PositiveInt

from . import db
from .users import find_user


class ChargeRequest(BaseModel):
    user_id: int
    amount_cents: PositiveInt
    currency: str = Field(min_length=3, max_length=3)


class RefundRequest(BaseModel):
    payment_id: str = Field(min_length=1)


class Payment(BaseModel):
    id: str
    user_id: int
    amount_cents: int
    currency: str
    status: Literal["charged", "refunded"]


def charge_payment(request: ChargeRequest) -> Payment:
    if not find_user(request.user_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="user not found",
        )

    payment = {
        "id": db.next_payment_id(),
        "user_id": request.user_id,
        "amount_cents": request.amount_cents,
        "currency": request.currency.upper(),
        "status": "charged",
    }
    db.payments[payment["id"]] = payment
    db.audit_log.append({"event": "payment_charged", "payment_id": payment["id"]})
    return Payment(**payment)


def refund_payment(request: RefundRequest) -> Payment:
    payment = db.payments.get(request.payment_id)
    if not payment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="payment not found",
        )

    payment["status"] = "refunded"
    db.audit_log.append({"event": "payment_refunded", "payment_id": payment["id"]})
    return Payment(**payment)
