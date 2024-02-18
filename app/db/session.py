from motor.motor_asyncio import AsyncIOMotorClient

class MongoDB:
    client: AsyncIOMotorClient = None # type: ignore
    db = None

mongo_db = MongoDB()

async def get_db():
    return mongo_db.db

def connect_to_mongo(uri:str, dbname: str):
    mongo_db.client = AsyncIOMotorClient(uri)
    mongo_db.db = mongo_db.client[dbname]

def close_mongo_connection():
    mongo_db.client.close()