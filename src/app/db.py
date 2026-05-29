from __future__ import annotations

from itertools import count
from typing import Any


users: dict[int, dict[str, Any]] = {
    1: {"id": 1, "email": "ada@example.com", "name": "Ada Lovelace"},
    2: {"id": 2, "email": "grace@example.com", "name": "Grace Hopper"},
}

payments: dict[str, dict[str, Any]] = {}
audit_log: list[dict[str, str]] = [{"event": "sandbox_started"}]

_payment_counter = count(1)


def next_payment_id() -> str:
    return f"pay_{next(_payment_counter)}"
