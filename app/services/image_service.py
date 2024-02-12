import os
from fastapi import HTTPException, UploadFile

async def save_image(id: str, flag: int, file: UploadFile):
    save_directory = "UPLOADS/"
    try:
        file_extension = file.filename.split('.')[-1]
        file_path = os.path.join(save_directory, f"{id}{flag}.{file_extension}")
        contents = await file.read()
        with open(file_path, "wb") as f:
            f.write(contents)
        await file.seek(0)
        return {"message": "File saved successfully"}
    except Exception as e:
        print(f"Error saving file: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to save file: {e}")