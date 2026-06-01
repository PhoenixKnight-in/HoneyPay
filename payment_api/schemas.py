from pydantic import BaseModel, field_validator
from decimal import Decimal
from datetime import datetime


# ── Auth ──────────────────────────────────────────────
class LoginRequest(BaseModel):
    username: str
    password: str

    @field_validator("username", "password")
    @classmethod
    def must_not_be_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Field cannot be empty")
        return v.strip()


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


# ── Balance ───────────────────────────────────────────
class BalanceResponse(BaseModel):
    username: str
    balance: Decimal

    class Config:
        from_attributes = True


# ── Transfer (Week 2) ─────────────────────────────────
class TransferRequest(BaseModel):
    receiver_username: str
    amount: Decimal

    @field_validator("amount")
    @classmethod
    def amount_must_be_positive(cls, v: Decimal) -> Decimal:
        if v <= 0:
            raise ValueError("Transfer amount must be greater than zero")
        return v
    
class TransactionResponse(BaseModel):
    id: int
    sender_id: int
    receiver_id: int
    amount: Decimal
    timestamp: datetime

    class Config:
        from_attributes = True