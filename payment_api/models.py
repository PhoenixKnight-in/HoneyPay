from sqlalchemy import Column, Integer, String, Numeric, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    password = Column(String(255), nullable=False)  # bcrypt hashed
    balance = Column(Numeric(12, 2), default=0)
    created_at = Column(TIMESTAMP, server_default=func.now())

    # Relationships
    sent_transactions = relationship(
        "Transaction",
        foreign_keys="Transaction.sender_id",
        back_populates="sender"
    )
    received_transactions = relationship(
        "Transaction",
        foreign_keys="Transaction.receiver_id",
        back_populates="receiver"
    )


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    sender_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    receiver_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    amount = Column(Numeric(12, 2), nullable=False)
    timestamp = Column(TIMESTAMP, server_default=func.now())

    sender = relationship(
        "User",
        foreign_keys=[sender_id],
        back_populates="sent_transactions"
    )
    receiver = relationship(
        "User",
        foreign_keys=[receiver_id],
        back_populates="received_transactions"
    )