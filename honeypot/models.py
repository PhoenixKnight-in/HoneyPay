from sqlalchemy import Column, Integer, String, Text, TIMESTAMP
from sqlalchemy.sql import func
from database import Base


class AttackLog(Base):
    __tablename__ = "attack_logs"

    id = Column(Integer, primary_key=True, index=True)
    ip_address = Column(String(45), nullable=False)
    endpoint = Column(String(100), nullable=False)
    payload = Column(Text, nullable=True)
    attack_type = Column(String(50), nullable=False)
    user_agent = Column(String(255), nullable=True)
    timestamp = Column(TIMESTAMP, server_default=func.now())