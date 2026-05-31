from pathlib import Path

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.staticfiles import StaticFiles

from .audit import audit_events
from .auth import require_admin
from .health import health_status, readiness_status
from .metadata import service_metadata
from .payments import ChargeRequest, Payment, RefundRequest, charge_payment, refund_payment
from .users import find_user


app = FastAPI(title="PR Review Sandbox")
frontend_dist = Path(__file__).resolve().parents[2] / "frontend" / "dist"


@app.get("/health")
def health() -> dict[str, str]:
    return health_status()


@app.get("/health/ready")
def ready() -> dict[str, object]:
    return readiness_status()


@app.get("/metadata")
def metadata() -> dict[str, object]:
    return service_metadata()


@app.get("/users/{id}")
def get_user(id: int) -> dict[str, object]:
    user = find_user(id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return user


@app.post("/payments/charge", response_model=Payment, response_model_exclude_none=True)
def charge(request: ChargeRequest) -> Payment:
    return charge_payment(request)


@app.post("/payments/refund", response_model=Payment, response_model_exclude_none=True)
def refund(request: RefundRequest) -> Payment:
    return refund_payment(request)


@app.get("/admin/audit-log", dependencies=[Depends(require_admin)])
def audit_log() -> dict[str, list[dict[str, str]]]:
    return {"events": audit_events()}


app.mount("/", StaticFiles(directory=frontend_dist, html=True, check_dir=False), name="frontend")
