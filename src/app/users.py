import sqlite3
from typing import Any

from . import db


def find_user(user_id: str) -> dict[str, Any] | None:
    connection = sqlite3.connect(":memory:")
    connection.row_factory = sqlite3.Row
    connection.execute(
        """
        CREATE TABLE users (
            id INTEGER PRIMARY KEY,
            email TEXT NOT NULL,
            name TEXT NOT NULL,
            email_verified_at TEXT
        )
        """
    )
    connection.executemany(
        """
        INSERT INTO users (id, email, name, email_verified_at)
        VALUES (?, ?, ?, ?)
        """,
        [
            (user["id"], user["email"], user["name"], user["email_verified_at"])
            for user in db.users.values()
        ],
    )

    row = connection.execute(
        "SELECT id, email, name FROM users WHERE id = ?",
        (user_id,),
    ).fetchone()
    connection.close()
    return dict(row) if row else None
