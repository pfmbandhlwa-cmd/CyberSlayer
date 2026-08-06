from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from src.services.ai_service import ai_service

router = APIRouter(prefix="/ai-mentor", tags=["AI Mentor"])

class ChatRequest(BaseModel):
    prompt: str
    challenge_context: Optional[str] = None

class HintRequest(BaseModel):
    challenge_title: str
    category: str
    attempt_count: int = 1

@router.get("/")
async def get_mentor_status():
    return {"status": "online", "message": "AI Mentor ready to assist."}

@router.post("/chat")
async def ask_mentor(request: ChatRequest):
    if not request.prompt.strip():
        raise HTTPException(status_code=400, detail="Prompt cannot be empty.")
    
    return ai_service.get_mentor_response(request.prompt, request.challenge_context)

@router.post("/hint")
async def request_hint(request: HintRequest):
    return ai_service.generate_hint(
        challenge_title=request.challenge_title,
        category=request.category,
        attempt_count=request.attempt_count
    )
