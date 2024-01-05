import os
os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"
import uvicorn
from fastapi import FastAPI, HTTPException, UploadFile, Form
from fastapi.responses import FileResponse, StreamingResponse
from starlette.middleware.cors import CORSMiddleware
from schemas import frontProfileSchema, sideProfileSchema, ImageOverviewSchema
from datetime import datetime
from pathlib import Path
import hashlib
import json
import io
import zipfile

import ProfileScoreCalcFront
import ProfileScoreCalcSide
import AutomateLandmarkFront
import AutomateLandmarkSide
import ImageOverviewCreate
import CreateReportImages
import Auth
import Payment

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

app.include_router(Auth.router, prefix="/api")
app.include_router(Payment.router, prefix="/cash")

@app.get('/')
def basic():
    return {"message":"Harmony Backend Run Successfully"}

@app.post('/getfrontscore')
def getFrontProfileScore(body:frontProfileSchema):
    return ProfileScoreCalcFront.mainProcess(body)

@app.post('/getsidescore')
def getSideProfileScore(body:sideProfileSchema):
    return ProfileScoreCalcSide.mainProcess(body)

@app.post('/frontmagic')
async def automateLandmarkFrontProfile(image:UploadFile):
    return AutomateLandmarkFront.mainProcess(image)

@app.post('/sidemagic')
async def automateLandmarkSideProfile(image:UploadFile):
    return AutomateLandmarkSide.mainProcess(image)

@app.post('/create')
async def createImageOverview(body:ImageOverviewSchema):
    return ImageOverviewCreate.mainProcess(body)

@app.post('/generate')
async def generateImageOverview(
    front:UploadFile = Form(...),
    side:UploadFile = Form(...),
    points: str = Form(...)):
    currentIndex = hashlib.md5(str(datetime.now()).encode()).hexdigest()

    # Save frontImage with currentIndex name
    frontImgPth = f"UPLOADS/{currentIndex}_0.jpg"
    with open(frontImgPth, "wb") as f:
        f.write(front.file.read())
    # Save sideImage with currentIndex name
    sideImgPth = f"UPLOADS/{currentIndex}_1.jpg"
    with open(sideImgPth, "wb") as f:
        f.write(side.file.read())
    await CreateReportImages.createReportImages(frontImgPth, sideImgPth, json.JSONDecoder().decode(points))

    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w") as zip_file:
        for i in range(1, 46):
            image_path = Path(f"REPORTS/{currentIndex}") / f"{i}.jpg"
            zip_file.write(image_path, arcname=image_path.name)
            print(image_path)

    # Rewind the buffer to the beginning
    zip_buffer.seek(0)

    headers = {
        "Content-Disposition": "attachment; filename=images.zip",
        "Content-Type": "application/zip",
    }
    
    return currentIndex
    return StreamingResponse(io.BytesIO(zip_buffer.read()), headers=headers)

@app.get('/image')
async def get_image_overview(hash: str, index: int):
    try:
        image_path = Path(f"REPORTS/{hash}") / f"{index}.jpg"
        if not image_path.is_file():
            raise HTTPException(status_code=404, detail="Image not found")
        return FileResponse(image_path, media_type="image/jpeg")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)