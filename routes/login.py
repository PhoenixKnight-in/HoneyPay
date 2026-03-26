from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database import get_db, User
from auth import verify_password, create_access_token

router = APIRouter()


# ── Request schema ────────────────────────────────────────────────────────────
class LoginRequest(BaseModel):
    username: str
    password: str


# ── POST /api/login ───────────────────────────────────────────────────────────
@router.post("/api/login")
def login(payload: LoginRequest, request: Request, db: Session = Depends(get_db)):
    # Input validation
    if not payload.username or not payload.password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username and password required")

    if len(payload.username) > 50:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid input")

    # Lookup user — SQLAlchemy parameterizes this automatically, no raw SQL
    user = db.query(User).filter(User.username == payload.username).first()

    # Always verify password even if user not found (prevents timing attacks)
    dummy_hash = "$2b$12$KIXsRqIzJmFnPQsNQETiveNJmBNf9vMCzR3oO1OwgFLEHFiAFnmNu"
    password_ok = verify_password(payload.password, user.password if user else dummy_hash)

    if not user or not password_ok:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"  # Same message for both cases — don't leak which failed
        )

    token = create_access_token(data={"sub": user.username, "user_id": user.id})

    return {
        "access_token": token,
        "token_type": "bearer"
    }