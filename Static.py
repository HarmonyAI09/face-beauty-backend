from fastapi import APIRouter
from pymongo import MongoClient
import os
from dotenv import load_dotenv
load_dotenv()

router = APIRouter()

mongoURL = os.getenv("MONGO_URL")
client = MongoClient(mongoURL)
db = client[os.getenv("DB")]
noteCollection = db[os.getenv("NOTE_COLLECTION")]

@router.get('/requirements')
async def getRequirements():
    requirements = noteCollection.find({"name":"photo_requirements"})
    requirementList = []
    for requirement in requirements:
        requirementList.extend(requirement.get('content', []))
    return requirementList

@router.get('/notes')
async def getNotes():
    notes = noteCollection.find({"name":"notes"})
    noteList = []
    for note in notes:
        noteList.extend(note.get('content', []))
    return noteList