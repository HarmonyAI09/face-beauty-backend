import uvicorn
from fastapi import FastAPI, UploadFile, Request
from starlette.middleware.cors import CORSMiddleware
from schemas import frontProfileSchema, sideProfileSchema, ImageOverviewSchema

import ProfileScoreCalcFront
import ProfileScoreCalcSide
import AutomateLandmarkFront
import AutomateLandmarkSide
import ImageOverviewCreate
import Auth
import Payment

app = FastAPI()

app.include_router(Auth.router, prefix="/api")
app.include_router(Payment.router, prefix="/")

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
    return True

@app.post('/create')
async def createImageOverview(body:ImageOverviewSchema):
    return ImageOverviewCreate.mainProcess(body)


if __name__ == "__main__":
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Allows all origins
        allow_credentials=True,
        allow_methods=["*"],  # Allows all methods
        allow_headers=["*"],  # Allows all headers
    )

    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)