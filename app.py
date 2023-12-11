import uvicorn
from fastapi import FastAPI, UploadFile, Request
from starlette.middleware.cors import CORSMiddleware
from schemas import frontProfileSchema, sideProfileSchema
import ProfileScoreCalcFront
import ProfileScoreCalcSide
import AutomateLandmarkFront
import AutomateLandmarkSide
import CreateCheckoutSession
import MyWebhookView
import Auth
import stripe
import os
from dotenv import load_dotenv

app = FastAPI()

app.include_router(Auth.router, prefix="/api")

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

@app.post('/create-checkout-session')
async def createCheckoutSession(request: Request):
    return CreateCheckoutSession.mainProcess(Request)

@app.post("/webhook")
async def myWebhookView(request: Request):
    return MyWebhookView.mainProcess(Request)

if __name__ == "__main__":
    load_dotenv()
    client = MongoClient(os.getenv("MONGO_URL"))
    db = client[os.getenv("DB_NAME")]
    users_collection = db[os.getenv("DB_COLLECTION")]
    

    stripe.api_key = os.getenv("STRIPE_KEY")
    endpoint_secret = os.getenv("WEBHOOK_SK")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Allows all origins
        allow_credentials=True,
        allow_methods=["*"],  # Allows all methods
        allow_headers=["*"],  # Allows all headers
    )

    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)