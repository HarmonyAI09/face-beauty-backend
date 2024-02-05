from fastapi import FastAPI
from .api.endpoints.user_router import router as user_router
from .db.session import connect_to_mongo, close_mongo_connection

app = FastAPI()

app.include_router(user_router)

@app.on_event("startup")
async def startup_event():
    connect_to_mongo("mongodb://localhost:27017", "mydatabase")

@app.on_event("shutdown")
async def shutdown_event():
    close_mongo_connection()