from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from dependencies import get_db
from core.security import verify_password, create_access_token
from core.rate_limiter import check_rate_limit
from schemas import LoginRequest, TokenResponse
import models

router = APIRouter(prefix="/api", tags=["Authentication"])


@router.post("/login", response_model=TokenResponse)
def login(
    request: Request,
    payload: LoginRequest,
    db: Session = Depends(get_db)
):
    """
    Authenticate a user and return a JWT access token.

    Security decisions:
    - Generic error message: never reveal which field was wrong
    - bcrypt verification: timing-safe comparison
    - Rate limiter: block IP after 5 failed attempts in 60 seconds
    - On success: reset the failed attempt counter for this IP
    """
    user = db.query(models.User).filter(
        models.User.username == payload.username
    ).first()

    if not user or not verify_password(payload.password, user.password):
        # Failed login — increment rate limit counter
        check_rate_limit(request, success=False)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    # Successful login — reset counter
    check_rate_limit(request, success=True)

    token = create_access_token(data={"sub": user.username})
    return TokenResponse(access_token=token)