"""Authentication API router."""

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from training_nomination.core.dependencies import get_current_user
from training_nomination.core.security import create_access_token, verify_password
from training_nomination.db.session import get_db
from training_nomination.models.user import User
from training_nomination.schemas.auth import LoginRequest, TokenResponse, UserResponse

router = APIRouter(prefix="/api/v1/auth", tags=["Authentication"])


@router.post("/login", response_model=TokenResponse)
def login(
    request: LoginRequest,
    response: Response,
    db: Session = Depends(get_db),
) -> TokenResponse:
    """Authenticate user with email and password, issuing a JWT access token."""
    user = db.query(User).filter(User.email == request.email.lower().strip()).first()
    if not user or not verify_password(request.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Issue JWT token
    token = create_access_token(
        data={
            "sub": user.id,
            "email": user.email,
            "role": user.role.name if user.role else "EMPLOYEE",
            "name": user.name,
        }
    )

    # Set cookie for browser UI convenience
    response.set_cookie(
        key="access_token",
        value=f"Bearer {token}",
        httponly=True,
        samesite="lax",
        secure=False,
    )

    return TokenResponse(
        access_token=token,
        token_type="bearer",
        user_id=user.id,
        name=user.name,
        email=user.email,
        role=user.role.name if user.role else "EMPLOYEE",
    )


@router.post("/logout")
def logout(response: Response) -> dict[str, str]:
    """Clear session cookie and logout."""
    response.delete_cookie(key="access_token")
    return {"message": "Successfully logged out."}


@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)) -> UserResponse:
    """Return profile information of the currently authenticated user."""
    return UserResponse(
        id=current_user.id,
        name=current_user.name,
        email=current_user.email,
        role=current_user.role.name if current_user.role else "EMPLOYEE",
        created_at=current_user.created_at,
    )
