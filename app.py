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
    return {"id" : currentIndex}
    
@app.get("/get_image/{id}/{image_index}")
async def get_image(id: str, image_index: int):
    file_path = f"REPORTS/{id}/{image_index}.jpg"
    return FileResponse(file_path, media_type="image/jpeg")

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)