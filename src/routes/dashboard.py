from fastapi import APIRouter

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

@router.get("/")
async def get_dashboard_stats():
    return {"user": "CyberSlayer", "completed_challenges": 0, "rank": "Novice"}
