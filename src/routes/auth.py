from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/auth", tags=["Authentication"])

class AuthRequest(BaseModel):
    username: str
    password: str

@router.post("/register")
async def register(user: AuthRequest):
    return {"message": f"User {user.username} registered successfully."}

@router.post("/login")
async def login(user: AuthRequest):
    return {"access_token": "dummy-token", "token_type": "bearer"}
