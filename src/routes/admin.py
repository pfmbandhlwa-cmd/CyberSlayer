from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from src.services.ai_service import ai_service

router = APIRouter(prefix="/api/ai", tags=["AI Mentor"])

class HintRequest(BaseModel):
    challenge_title: str
    challenge_description: str
    user_question: str

class DefinitionRequest(BaseModel):
    term: str

@router.post("/hint")
async def get_socratic_hint(payload: HintRequest):
    """Returns a Socratic hint without giving away direct flags or solutions."""
    if not payload.user_question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty.")
        
    hint = ai_service.generate_socratic_hint(
        challenge_title=payload.challenge_title,
        description=payload.challenge_description,
        user_query=payload.user_question
    )
    return {"status": "success", "hint": hint}

@router.post("/define")
async def get_term_definition(payload: DefinitionRequest):
    """Provides a quick 2-sentence definition for highlighted cybersecurity terms."""
    if not payload.term.strip():
        raise HTTPException(status_code=400, detail="Term cannot be empty.")
        
    # Optional helper method on ai_service if implemented
    definition = ai_service.define_term(payload.term) if hasattr(ai_service, 'define_term') else f"Concept lookup for '{payload.term}'."
    return {"status": "success", "term": payload.term, "definition": definition}