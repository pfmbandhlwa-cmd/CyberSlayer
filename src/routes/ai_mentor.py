from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional

router = APIRouter(prefix="/ai-mentor", tags=["AI Mentor"])

class ChatRequest(BaseModel):
    prompt: str
    challenge_context: Optional[str] = None

@router.get("/")
async def get_mentor_status():
    return {"status": "online", "message": "AI Mentor ready to assist."}

@router.post("/chat")
async def ask_mentor(request: ChatRequest):
    if not request.prompt.strip():
        raise HTTPException(status_code=400, detail="Prompt cannot be empty.")
    
    # Placeholder response until ai_service integration is wired up
    return {
        "reply": f"Mentor guidance for: '{request.prompt}'",
        "context": request.challenge_context
    }
