from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from pymongo import MongoClient
from datetime import datetime, timedelta
from bson import ObjectId

router = APIRouter()

mongo_uri = "mongodb://localhost:27017/"
client = MongoClient(mongo_uri)

# Create a database object
db = client["harmony"]

# Define MongoDB collection for users
users_collection = db["users"]

class PurchasePlan(BaseModel):
    email: str

def calculate_expiration_date():    
    return datetime.now() + timedelta(days=30)

@router.post("/buy-premium")
def buy_premium(purchase_data: PurchasePlan):
    email = purchase_data.email
    expire_date = calculate_expiration_date()
    result = users_collection.update_one({"email": email}, {"$set": {"lvl": 1, "expire_day": expire_date}})
    if result.modified_count:
        return {"message": "Premium plan purchased successfully, expires on: " + expire_date.strftime("%Y-%m-%d")}
    else:
        raise HTTPException(status_code=404, detail="User not found or already on premium level")

@router.post("/buy-professional")
def buy_professional(purchase_data: PurchasePlan):
    email = purchase_data.email
    expire_date = calculate_expiration_date()
    result = users_collection.update_one({"email": email}, {"$set": {"lvl": 2, "expire_day": expire_date}})
    if result.modified_count:
        return {"message": "Professional plan purchased successfully, expires on: " + expire_date.strftime("%Y-%m-%d")}
    else:
        raise HTTPException(status_code=404, detail="User not found or already on professional level")

@router.get("/")
def helps():
    return {"message": "Connection successful"}
