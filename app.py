import uvicorn
from fastapi import FastAPI, UploadFile
from starlette.middleware.cors import CORSMiddleware
from schemas import frontProfileSchema, sideProfileSchema
import ProfileScoreCalcFront
import ProfileScoreCalcSide

app = FastAPI()

@app.post('/getfrontscore')
def getFrontProfileScore(body:frontProfileSchema):
    return ProfileScoreCalcFront.mainProcess(body)

@app.post('/getsidescore')
def getSideProfileScore(body:sideProfileSchema):
    return ProfileScoreCalcSide.mainProcess(body)

@app.post('/frontmagic')
async def automateLandmarkFrontProfile(image:UploadFile):
    return {"result":"success"}

if __name__ == "__main__":
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Allows all origins
        allow_credentials=True,
        allow_methods=["*"],  # Allows all methods
        allow_headers=["*"],  # Allows all headers
    )

    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)