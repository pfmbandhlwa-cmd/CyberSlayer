from sqlalchemy import Column, Integer, ForeignKey, DateTime, UniqueConstraint
from datetime import datetime
from src.database.db import Base

class UserProgress(Base):
    __tablename__ = "user_progress"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    challenge_id = Column(Integer, ForeignKey("challenges.id"), nullable=False)
    solved_at = Column(DateTime, default=datetime.utcnow)

    __table_args__ = (UniqueConstraint('user_id', 'challenge_id', name='_user_challenge_uc'),)
