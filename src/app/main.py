from fastapi import Depends, FastAPI, HTTPException, status

from . import db
from .auth import require_admin
from .payments import ChargeRequest, Payment, RefundRequest, charge_payment, refund_payment
from .users import find_user


app = FastAPI(title="PR Review Sandbox")


@app.get("/users/{id}")
def get_user(id: int) -> dict[str, object]:
    user = find_user(id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="user not found",
        )
    return user


@app.post("/payments/charge", response_model=Payment)
def charge(request: ChargeRequest) -> Payment:
    return charge_payment(request)


@app.post("/payments/refund", response_model=Payment)
def refund(request: RefundRequest) -> Payment:
    return refund_payment(request)


@app.get("/admin/audit-log", dependencies=[Depends(require_admin)])
def audit_log() -> dict[str, list[dict[str, str]]]:
    return {"events": list(db.audit_log)}
