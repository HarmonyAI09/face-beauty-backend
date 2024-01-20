from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from pymongo import MongoClient

router = APIRouter()
mongo_uri = MONGO_URL
client = MongoClient(mongo_uri)
db = client[DB_NAME]
users_collection = db[USER_COLLECTION]

class UserSignIn(BaseModel):
    email: str
    password: str

class UserSignUp(BaseModel):
    username: str
    email: str
    password: str

@router.post("/signin")
def sign_in(user: UserSignIn):
    # Find the user by email and password in the MongoDB collection
    result = users_collection.find_one({"email": user.email, "password": user.password})

    if result:
        return {"message": "Sign-in successful", "name": result["username"], "mail": result["email"], "level": result["lvl"], "expire": result["expire_day"]}
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")

@router.post("/signup")
def sign_up(user: UserSignUp):
    # Check if the username or email already exists in the MongoDB collection
    existing_user = users_collection.find_one({"$or": [{"username": user.username}, {"email": user.email}]})

    if existing_user:
        raise HTTPException(status_code=400, detail="Username or email already exists")

    new_user = {
        "username": user.username,
        "email": user.email,
        "password": user.password,
        "lvl": 0,
        "expire_day": None
    }
    users_collection.insert_one(new_user)

    return {"message": "Sign-up successful"}