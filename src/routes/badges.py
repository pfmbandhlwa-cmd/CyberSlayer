from fastapi import APIRouter

router = APIRouter(prefix="/badges", tags=["Badges"])

@router.get("/")
async def get_badges():
    return {"badges": []}
