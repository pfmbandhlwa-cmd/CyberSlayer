from fastapi import APIRouter, HTTPException
from src.models.challenge import AnswerSubmission, ChallengeCreate
from src.services.challenge_service import challenge_service

router = APIRouter(tags=["Challenges"])

@router.get("/challenges")
def fetch_challenges():
    return {"challenges": challenge_service.list_challenges()}

@router.get("/stats")
def fetch_stats():
    return challenge_service.get_stats()

@router.post("/challenges")
def create_challenge(challenge: ChallengeCreate):
    if challenge.correct_option.upper() not in ["A", "B", "C", "D"]:
        raise HTTPException(status_code=400, detail="Correct option must be A, B, C, or D")
        
    new_id = challenge_service.create(challenge.model_dump())
    return {"status": "SUCCESS", "message": "Challenge added successfully", "challenge_id": new_id}

@router.post("/challenges/{challenge_id}/submit")
def submit_answer(challenge_id: int, submission: AnswerSubmission):
    return challenge_service.verify_answer(submission.challenge_id, submission.selected_option)

@router.post("/answer")
def submit_answer_legacy(challenge_id: int, submission: AnswerSubmission):
    return challenge_service.verify_answer(submission.challenge_id, submission.selected_option)