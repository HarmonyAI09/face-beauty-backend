import os
os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"
import uvicorn
from fastapi import FastAPI, HTTPException, UploadFile, Form
from fastapi.responses import FileResponse, StreamingResponse
from starlette.middleware.cors import CORSMiddleware
from schemas import frontProfileSchema, sideProfileSchema, ImageOverviewSchema
from ReportProcess import ReportStoreSchema
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


mongoURL = os.getenv("MONGO_URL")
client = MongoClient(mongoURL)
db = client[os.getenv("DB")]
userCollection = db[os.getenv("USER_COLLECTION")]
reportCollection = db[os.getenv("REPORT_COLLECTION")]


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

    currentDirectory = os.path.dirname(__file__)
    uploadFolderPath = os.path.join(currentDirectory, os.getenv("UPLOAD_FOLDER"))
    front_img_name = f"{currentIndex}_0.jpg"
    side_img_name = f"{currentIndex}_1.jpg"
    front_img_path = os.path.join(uploadFolderPath, front_img_name)
    side_img_path = os.path.join(uploadFolderPath, side_img_name)

    print({currentDirectory, uploadFolderPath, front_img_name, side_img_name})

    # Save frontImage with currentIndex name
    with open(front_img_path, "wb") as f:
        f.write(front.file.read())
    # Save sideImage with currentIndex name
    with open(side_img_path, "wb") as f:
        f.write(side.file.read())
    await CreateReportImages.createReportImages(front_img_path, side_img_path, json.JSONDecoder().decode(points))    
    return {"id" : currentIndex}
    
@app.get("/get_image/{id}/{image_index}")
async def get_image(id: str, image_index: int):
    file_path = f"REPORTS/{id}/{image_index}.jpg"
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

@app.get("/reports/{mail}")
async def getReportsByEmail(mail: str):
    return ReportStoreSchema.getReports(mail)

@app.get("/details/{id}")
async def getDetails(id: str):
    return ReportStoreSchema.getDetails(id)

@app.get("/download/{rid}")
async def downloadReport(rid: str):
    xlsx_download_base_path = os.path.join(os.getcwd(), "XLSX")
    if not os.path.exists(xlsx_download_base_path):
        os.mkdir(xlsx_download_base_path)

    def saveXlsx(filename):
        workbook = Workbook()
        workbook.remove_sheet(workbook.active)
        sheet = workbook.create_sheet('Front Profile')
        sheet['a1'] = 'Image'
        sheet['b1'] = 'Measure Name'
        sheet['c1'] = 'Value'
        sheet['d1'] = 'Score'
        sheet['e1'] = 'Ideal Range'
        sheet['f1'] = 'Meaning'
        sheet['g1'] = 'Advice'

        workbook.save(filename=os.path.join(xlsx_download_base_path, filename))
        workbook.close()
    
    saveXlsx(f'{rid}.xlsx')
    
    return {"ok": True}



if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)