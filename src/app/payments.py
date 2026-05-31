from typing import Literal

from fastapi import HTTPException, status
from pydantic import BaseModel, ConfigDict, Field, PositiveInt, field_validator

from . import db
from .users import find_user


class ChargeRequest(BaseModel):
    user_id: int
    amount_cents: PositiveInt
    currency: str = Field(min_length=3, max_length=3)
    description: str | None = None


class RefundRequest(BaseModel):
    model_config = ConfigDict(validate_default=True)

    payment_id: str = Field(min_length=1)
    reason: str | None = None

    @field_validator("reason")
    @classmethod
    def normalize_reason(cls, value: str | None) -> str:
        if value is None:
            return "unspecified"

        reason = value.strip()
        if not reason:
            return "unspecified"
        if len(reason) > 200:
            raise ValueError("reason must be 200 characters or fewer")
        return reason


class Payment(BaseModel):
    id: str
    user_id: int
    amount_cents: int
    currency: str
    status: Literal["charged", "refunded"]
    description: str | None = None
    refund_reason: str | None = None


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
        "description": request.description,
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
    payment["refund_reason"] = request.reason
    db.audit_log.append(
        {
            "event": "payment_refunded",
            "payment_id": payment["id"],
            "reason": request.reason,
        }
    )
    return Payment(**payment)
