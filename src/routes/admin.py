from fastapi import APIRouter
from src.services.ai_service import ai_service

router = APIRouter(prefix="/admin", tags=["Admin"])

@router.get("/")
async def get_admin_status():
    return {"status": "Admin panel active"}
