"""FastAPI security dependencies and Role-Based Access Control (RBAC)."""

from collections.abc import Callable

from fastapi import Cookie, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from training_nomination.core.security import decode_access_token
from training_nomination.db.session import get_db
from training_nomination.models.user import User

bearer_scheme = HTTPBearer(auto_error=False)


def get_token_from_request(
    auth: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    access_token: str | None = Cookie(default=None),
) -> str | None:
    """Extract token from Authorization header or cookie."""
    if auth and auth.credentials:
        return auth.credentials
    if access_token:
        # Strip potential Bearer prefix if stored in cookie
        if access_token.startswith("Bearer "):
            return access_token.split(" ", 1)[1]
        return access_token
    return None


def get_current_user_optional(
    token: str | None = Depends(get_token_from_request),
    db: Session = Depends(get_db),
) -> User | None:
    """Return authenticated user or None if unauthenticated."""
    if not token:
        return None
    payload = decode_access_token(token)
    if not payload:
        return None
    user_id: str = payload.get("sub")
    if not user_id:
        return None
    user = db.query(User).filter(User.id == user_id).first()
    return user


def get_current_user(
    user: User | None = Depends(get_current_user_optional),
) -> User:
    """Require valid authenticated user."""
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication credentials were not provided or are invalid.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


def require_roles(allowed_roles: list[str]) -> Callable[[User], User]:
    """Dependency factory checking user role against allowed list."""

    def role_checker(current_user: User = Depends(get_current_user)) -> User:
        if not current_user.role or current_user.role.name not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access forbidden: requires one of roles {allowed_roles}",
            )
        return current_user

    return role_checker
