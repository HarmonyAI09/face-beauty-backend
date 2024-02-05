from fastapi import APIRouter, Depends
from ...db.schemas.user_schema import UserRead
from ...services.user_service import get_users

router = APIRouter()

@router.get("/users", response_model=list[UserRead])
async def read_users():
    return await get_users()