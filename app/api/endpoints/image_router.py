from fastapi import APIRouter, File, Form, HTTPException, UploadFile, status

from ...db.schemas.image_schema import ImageRegistration
from ...services.image_service import save_image

router = APIRouter()

@router.post('/register')
async def register_image(file: UploadFile = Form(...), id: str = Form(...), flag: int = Form(...)):
    try:
        return await save_image(id, flag, file)
    except Exception as e:
        print(f"Error saving image: {e}")
        raise HTTPException(status_code=422, detail=str(e))