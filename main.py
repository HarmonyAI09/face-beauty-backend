import os

from app.services.draw_service import CompleteMarkPoints, GetReferenceLines
os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"
import uvicorn
from fastapi import FastAPI, HTTPException, UploadFile, Form
from fastapi.responses import FileResponse, StreamingResponse
from starlette.middleware.cors import CORSMiddleware
from schemas import frontProfileSchema, sideProfileSchema, ImageOverviewSchema
from ReportProcess import ReportStoreSchema, ReportSaveSchema, ReportFrontSideSaveSchema
from datetime import datetime, date
from dotenv import load_dotenv
from pathlib import Path
import hashlib
import json
from pymongo import MongoClient
from openpyxl import Workbook

import ProfileScoreCalcFront
import ProfileScoreCalcSide
import AutomateLandmarkFront
import AutomateLandmarkSide
import ImageOverviewCreate
import CreateReportImages
import Auth
import Payment
import Static

from app.api.endpoints.image_router import router as image_router
from app.api.endpoints.profile_router import router as profile_router
from app.api.endpoints.user_router import router as user_router
from app.db.session import connect_to_mongo, close_mongo_connection


mongoURL = os.getenv("MONGO_URL")
client = MongoClient(mongoURL)
db = client[os.getenv("DB")]
userCollection = db[os.getenv("USER_COLLECTION")]
reportCollection = db[os.getenv("REPORT_COLLECTION")]
storeCollection = db[os.getenv("STORE_COLLECTION")]


app = FastAPI()
load_dotenv()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

app.include_router(Auth.router, prefix="/api")
app.include_router(Payment.router)
app.include_router(Static.router, prefix="/static")
app.include_router(image_router, prefix="/image")
app.include_router(profile_router, prefix="/profile")
app.include_router(user_router, prefix="/user")

@app.on_event("startup")
async def startup_event():
    connect_to_mongo("mongodb+srv://admin:trustkmp123@cluster0.celqdib.mongodb.net", "harmony")

@app.on_event("shutdown")
async def shutdown_event():
    close_mongo_connection()

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

@app.post('/repair')
async def RepairLandmarks(points: list = Form(...)):
    points = json.loads(points[0])
    points = points['markPoints']
    RLs = GetReferenceLines(points)
    points = CompleteMarkPoints(points, RLs)
    return {"points": points, "RLs": RLs}

@app.post('/generate')
async def generateImageOverview(id: str = Form(...), points: str = Form(...)):
    print(points)
    currentDirectory = os.path.dirname(__file__)
    uploadFolderPath = os.path.join(currentDirectory, os.getenv("UPLOAD_FOLDER"))
    front_img_name = f"{id}0.jpg"
    side_img_name = f"{id}1.jpg"
    front_img_path = os.path.join(uploadFolderPath, front_img_name)
    side_img_path = os.path.join(uploadFolderPath, side_img_name)

    print(json.JSONDecoder().decode(points))
    await CreateReportImages.createReportImages(front_img_path, side_img_path, json.JSONDecoder().decode(points)) 
    return {"id" : id}
    
@app.get("/get_image/{id}/{image_index}")
async def get_image(id: str, image_index: int):
    file_path = f"UPLOADS/{id}/{image_index}.jpg"
    return FileResponse(file_path, media_type="image/jpeg")

@app.get("/get_image/{id}{flag}")
async def src_image(id: str, flag: int):
    file_path = f"UPLOADS/{id}{flag}.jpg"
    return FileResponse(file_path, media_type="image/jpeg")

@app.get("/uploads/{file_name}")
async def get_file(file_name: str):
    file_path = f"UPLOADS/{file_name}"
    return FileResponse(file_path)

@app.post('/save')
async def saveReport(frontImage:UploadFile = Form(...),
    sideImage:UploadFile = Form(...),
    mail: str = Form(...),
    reportID: str = Form(...),
    gender: str = Form(...),
    race: str = Form(...),
    reportOwner: str = Form(...),
    keyPoints: list = Form(...)):

    def userCanSave(email):
        found_user = userCollection.find_one({"email": email})
        if not found_user:
            return False
        if found_user["lvl"] == 0:
            return False
        if found_user["expire_day"].date() < datetime.now().date():
            return False
        
        found_report = reportCollection.find_one({"mail": email})
        if found_report and len(found_report["reports"]) >= 5:
            return False
        return True
    
    if userCanSave(mail) == False:
        return {"success": False, "error": "Please upgrade your tier"}

    currentIndex = hashlib.md5(str(datetime.now()).encode()).hexdigest()

    # Save images
    try:
        currentDirectory = os.path.dirname(__file__)
        uploadFolderPath = os.path.join(currentDirectory, os.getenv("UPLOAD_FOLDER"))

        front_img_name = f"{currentIndex}_0.jpg"
        side_img_name = f"{currentIndex}_1.jpg"
        front_img_path = os.path.join(uploadFolderPath, front_img_name)
        side_img_path = os.path.join(uploadFolderPath, side_img_name)

        with open(front_img_path, "wb") as f:
            f.write(frontImage.file.read())
        with open(side_img_path, "wb") as f:
            f.write(sideImage.file.read())
    except Exception as e:
        print(f"File saving error {e}")
    
    body = ReportStoreSchema(
        mail = mail,
        reportID = reportID,
        gender = gender,
        race = race,
        reportOwner = reportOwner,
        keyPoints = keyPoints,
        frontImage = front_img_name,
        sideImage = side_img_name
        )

    return body.store()

@app.post('/store')
async def storeReport(body: ReportSaveSchema):
    data = {
        "report_id": body.report_id,
        "gender": body.gender,
        "name": body.name,
        "percentage": body.percentage,
        "race": body.race,
        "score": body.score
    }
    storeCollection.insert_one(data)
    return body

@app.post('/store/{frontOrSide}')
async def storeReportFront(body: ReportFrontSideSaveSchema, frontOrSide: str):
    result = storeCollection.update_one(
        {"report_id": body.report_id},
        {"$set": {frontOrSide: body.profile_data}}
        )
    return result.modified_count

@app.get("/reports/{mail}")
async def getReportsByEmail(mail: str):
    return ReportStoreSchema.getReports(mail)

@app.get("/details/{id}")
async def getDetails(id: str):
    return ReportStoreSchema.getDetails(id)

@app.get("/store/{id}")
async def getProfile(id: str):
    return {"message": "Hello world"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)