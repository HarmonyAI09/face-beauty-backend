import os
from fastapi import HTTPException, UploadFile
from PIL import Image
import io

async def save_image(id: str, flag: int, file: UploadFile):
    save_directory = "UPLOADS/"
    if not os.path.exists(save_directory):
        os.makedirs(save_directory)

    try:
        file_path = os.path.join(save_directory, f"{id}{flag}.jpg")
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))
        image = image.convert('RGB')
        image.save(file_path, 'JPEG')
        await file.seek(0)
        return {"message": "File saved successfully as JPG"}
    except Exception as e:
        print(f"Error saving file: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to save file as JPG: {e}")