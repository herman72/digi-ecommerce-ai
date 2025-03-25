from fastapi import APIRouter

router = APIRouter()

@router.post("create-category")
async def create_category()