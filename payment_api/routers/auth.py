from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from dependencies import get_db
from core.security import verify_password, create_access_token
from schemas import LoginRequest, TokenResponse
import models

router = APIRouter(prefix="/api", tags=["Authentication"])


@router.post("/login", response_model=TokenResponse)
def login(request: Request, payload: LoginRequest, db: Session = Depends(get_db)):
    """
    Authenticate a user and return a JWT access token.

    Security decisions:
    - Generic error message: never reveal whether username or password was wrong
    - bcrypt verification: timing-safe comparison
    - JWT issued only on success
    """
    # Look up user by username
    user = db.query(models.User).filter(
        models.User.username == payload.username
    ).first()

    # Intentionally vague error — don't reveal which field was wrong
    if not user or not verify_password(payload.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    token = create_access_token(data={"sub": user.username})

    return TokenResponse(access_token=token)