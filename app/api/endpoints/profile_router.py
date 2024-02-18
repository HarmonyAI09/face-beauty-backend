from fastapi import APIRouter
from pydantic import EmailStr

from app.db.schemas.profile_schema import ProfileRead, ProfileReg
from app.services.profile_service import add_profile, download_report, get_profile, get_report


router = APIRouter()

@router.post('/register', response_model = ProfileRead)
async def register_profile(info: ProfileReg):
    return await add_profile(info)

@router.get('/{mail}', response_model = ProfileRead)
async def get(mail: EmailStr):
    return await get_profile(mail)

@router.get('/report/{id}')
async def get(id: str):
    return await get_report(id)

@router.get('/download/{id}')
async def download(id: str):
    return await download_report(id)