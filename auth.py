from fastapi import APIRouter
from schemas import UserSchema, PremiumSchema
from datetime import datetime, timedelta
from pymongo import MongoClient
import os

from dotenv import load_dotenv
load_dotenv()

router = APIRouter()

mongoURL = os.getenv("MONGO_URL")
client = MongoClient(mongoURL)
db = client[os.getenv("DB")]
userCollection = db[os.getenv("DB_COLLECTION")]

@router.post("/signin")
def signIn(user : UserSchema):
    one = userCollection.find_one({"email": user.mail, "password": user.password})
    if one:
        return {"success":True, "status": "Sign-in success.", "name": one["username"], "mail": one["email"], "level": one["lvl"], "expire": one["expire_day"]} 
    else:
        return {"success":False, "status": "Sign-in failed."}
    
@router.post("/signup")
def signUp(user : UserSchema):
    one = userCollection.find_one({"email": user.mail})
    if one:
        return {"success":False, "status": "Already exists."}
    else:
        new = {
            "username" : user.name,
            "email" : user.mail,
            "password" : user.pswd,
            "lvl" : 0,
            "expire_day" : None
        }
        userCollection.insert_one(new)
        return {"success":True, "status": "Sign-up success."}
    
def update(user : PremiumSchema):
    return userCollection.update_one({"email": user.mail}, {"$set": {"lvl": user.plan, "expire_day": datetime.now() + timedelta(days=30)}})