from typing import Any

from . import db


def find_user(user_id: int) -> dict[str, Any] | None:
    user = db.users.get(user_id)
    return user.copy() if user else None
