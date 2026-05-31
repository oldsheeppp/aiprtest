from typing import Any

from . import db
from .settings import SERVICE_NAME, SERVICE_VERSION


def health_status() -> dict[str, str]:
    return {
        "service": SERVICE_NAME,
        "status": "ok",
        "version": SERVICE_VERSION,
    }


def readiness_status() -> dict[str, Any]:
    return {
        "ready": True,
        "checks": {
            "users": len(db.users),
            "payments": len(db.payments),
            "audit_events": len(db.audit_log),
        },
    }
