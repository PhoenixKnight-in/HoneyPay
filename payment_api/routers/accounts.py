from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from dependencies import get_db, get_current_user
from schemas import BalanceResponse, TransferRequest, TransactionResponse
import models

router = APIRouter(prefix="/api", tags=["Accounts"])


@router.get("/balance", response_model=BalanceResponse)
def get_balance(current_user: models.User = Depends(get_current_user)):
    """
    Return the authenticated user's current balance.
    User object already loaded by get_current_user — no extra DB query needed.
    """
    return BalanceResponse(
        username=current_user.username,
        balance=current_user.balance
    )


@router.post("/transfer", status_code=status.HTTP_200_OK)
def transfer(
    payload: TransferRequest,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """
    Transfer money from authenticated user to another user.

    Security decisions:
    - Cannot transfer to yourself
    - Cannot transfer more than your balance
    - Amount must be positive (validated in schema)
    - Both balance updates happen in one atomic transaction
    """

    # Guard: no self-transfer
    if payload.receiver_username == current_user.username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot transfer to yourself"
        )

    # Look up receiver
    receiver = db.query(models.User).filter(
        models.User.username == payload.receiver_username
    ).first()

    if not receiver:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Receiver not found"
        )

    # Guard: insufficient funds
    if current_user.balance < payload.amount:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Insufficient balance"
        )

    # Atomic transfer — both updates or neither
    try:
        current_user.balance -= payload.amount
        receiver.balance += payload.amount

        log = models.Transaction(
            sender_id=current_user.id,
            receiver_id=receiver.id,
            amount=payload.amount
        )
        db.add(log)
        db.commit()

    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Transfer failed. Please try again."
        )

    return {
        "message": "Transfer successful",
        "transferred": float(payload.amount),
        "to": receiver.username,
        "remaining_balance": float(current_user.balance)
    }


@router.get("/transactions", response_model=list[TransactionResponse])
def get_transactions(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """
    Return all transactions where the user was sender or receiver.
    Ordered by most recent first.
    """
    transactions = db.query(models.Transaction).filter(
        (models.Transaction.sender_id == current_user.id) |
        (models.Transaction.receiver_id == current_user.id)
    ).order_by(models.Transaction.timestamp.desc()).all()

    return transactions