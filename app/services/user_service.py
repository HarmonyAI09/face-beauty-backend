from fastapi import HTTPException
from pydantic import EmailStr

from ..db.session import get_db
from ..db.schemas.user_schema import UserCreate, UserLogin
from ..core.security import hash_password, verify_password

async def get_users():
    db = get_db()
    users_collection = db["users"]
    users = users_collection.find().to_list(100)
    return users

async def create_user(user_data: UserCreate):
    db = get_db()
    users_collection = db["users"]

    # Check if the email is already in use
    existing_user = await users_collection.find_one({"email": user_data.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Hash the user's password before storing it
    hashed_password = hash_password(user_data.password)

    # Create new user document
    new_user = await users_collection.insert_one({
        "name": user_data.name,
        "email": user_data.email,
        "hashed_password": hashed_password,
        "level": 0,
        "expire_date": None
    })

    # Fetch the new user and return it
    created_user = await users_collection.find_one({"_id": new_user.inserted_id})
    return created_user

async def authenticate_user(user_credentials: UserLogin):
    db = get_db()
    users_collection = db["users"]

    # Fetch the user by email
    user = await users_collection.find_one({"email": user_credentials.email})
    if not user:
        return None
    
    # Verify the password
    if not verify_password(user_credentials.password, user["hashed_password"]):
        return None
    
    return user

async def update_user_info(user_id: str, user_update: dict):
    db = get_db()
    users_collection = db["users"]
    await users_collection.update_one({"_id": user_id}, {"$set": user_update})
    updated_user = await users_collection.find_one({"_id": user_id})
    return updated_user

async def update_as_premium(email: EmailStr):
    db = await get_db()
    users_collection = db['users']
    await users_collection.update_one({"email":email}, {"$set": {"lvl": 1}})