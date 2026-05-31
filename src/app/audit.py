from . import db


def audit_events() -> list[dict[str, str]]:
    return list(db.audit_log)
