from sqlalchemy import Column, Integer, String, Boolean, Text
from src.database.db import Base

class Challenge(Base):
    __tablename__ = "challenges"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    category = Column(String(50), nullable=False, index=True)  # e.g., sqli, xss, crypto
    difficulty = Column(String(20), nullable=False, default="Medium")  # Easy, Medium, Hard
    points = Column(Integer, nullable=False, default=100)
    description = Column(Text, nullable=False)
    flag = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)

    def to_dict(self):
        """Converts model instance to dictionary (excluding flag for safety)."""
        return {
            "id": self.id,
            "title": self.title,
            "category": self.category,
            "difficulty": self.difficulty,
            "points": self.points,
            "description": self.description,
            "is_active": self.is_active
        }
