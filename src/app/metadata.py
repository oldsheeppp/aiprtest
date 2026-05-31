from typing import Any

from .settings import CAPABILITIES, ENVIRONMENT, SERVICE_NAME


def service_metadata() -> dict[str, Any]:
    return {
        "service": SERVICE_NAME,
        "environment": ENVIRONMENT,
        "capabilities": list(CAPABILITIES),
    }
