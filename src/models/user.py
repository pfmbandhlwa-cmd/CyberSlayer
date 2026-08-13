from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from src.database.db import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(100), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    score = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
