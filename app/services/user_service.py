from ..db.session import get_db

async def get_users():
    db = get_db()
    user_collection = db["users"]
    users = user_collection.find().to_list(100)
    return users