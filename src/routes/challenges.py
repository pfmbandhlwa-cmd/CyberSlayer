from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List

router = APIRouter(prefix="/challenges", tags=["Challenges"])

CHALLENGES_DB = [
    {
        "id": 1,
        "title": "SQLi Authentication Bypass",
        "category": "sqli",
        "difficulty": "Easy",
        "points": 100,
        "description": "Bypass the login form by exploiting vulnerable payload input fields.",
        "solved": False
    },
    {
        "id": 2,
        "title": "Reflected XSS Search Portal",
        "category": "xss",
        "difficulty": "Medium",
        "points": 250,
        "description": "Inject an executable script parameter into the search query.",
        "solved": False
    },
    {
        "id": 3,
        "title": "Base64 Header Decoder",
        "category": "crypto",
        "difficulty": "Easy",
        "points": 100,
        "description": "Extract and decode the encoded secret key stored in the response header.",
        "solved": False
    }
]

class FlagSubmission(BaseModel):
    flag: str

@router.get("/")
async def list_challenges():
    return {"status": "success", "challenges": CHALLENGES_DB}

@router.post("/{challenge_id}/submit")
async def submit_flag(challenge_id: int, payload: FlagSubmission):
    # Validates flag against target challenge pattern
    expected_flag = f"cyber{{flag_{challenge_id}_solved}}"
    if payload.flag.strip() == expected_flag:
        return {"status": "success", "correct": True, "message": "Flag captured! Points added."}
    return {"status": "incorrect", "correct": False, "message": "Invalid flag format or value."}
