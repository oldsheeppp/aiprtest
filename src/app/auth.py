from typing import Annotated

from fastapi import Header, HTTPException, status


def require_admin(x_role: Annotated[str | None, Header(alias="X-Role")] = None) -> None:
    if x_role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="admin role required",
        )
