from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional

from src.database.db import get_db
from src.models.challenge import Challenge

router = APIRouter(prefix="/challenges", tags=["Challenges"])

class FlagSubmission(BaseModel):
    flag: str

class ChallengeCreate(BaseModel):
    title: str
    category: str
    difficulty: str = "Medium"
    points: int = 100
    description: str
    flag: str

@router.get("/")
async def list_challenges(category: Optional[str] = None, db: Session = Depends(get_db)):
    query = db.query(Challenge).filter(Challenge.is_active == True)
    if category:
        query = query.filter(Challenge.category == category.lower())
    
    challenges = query.all()
    return {"status": "success", "challenges": [c.to_dict() for c in challenges]}

@router.post("/{challenge_id}/submit")
async def submit_flag(challenge_id: int, payload: FlagSubmission, db: Session = Depends(get_db)):
    challenge = db.query(Challenge).filter(Challenge.id == challenge_id, Challenge.is_active == True).first()
    if not challenge:
        raise HTTPException(status_code=404, detail="Challenge not found.")

    if payload.flag.strip() == challenge.flag:
        return {
            "status": "success",
            "correct": True,
            "message": f"Correct flag! You earned {challenge.points} points.",
            "points": challenge.points
        }

    return {
        "status": "incorrect",
        "correct": False,
        "message": "Invalid flag. Review payload execution and try again."
    }

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_challenge(new_challenge: ChallengeCreate, db: Session = Depends(get_db)):
    db_item = Challenge(**new_challenge.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return {"status": "success", "challenge": db_item.to_dict()}
