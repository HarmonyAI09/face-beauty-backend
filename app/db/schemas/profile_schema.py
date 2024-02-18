from datetime import datetime
from pydantic import BaseModel, EmailStr
from typing import List

class ProfileReg(BaseModel):
    mail: EmailStr
    profileID: str
    name: str
    gender: str
    racial: str

class ProfileID(BaseModel):
    id: str
    dateAdded: str
    name: str
    gender: str
    racial: str

class ProfileRead(BaseModel):
    mail: EmailStr
    profileIDs: List[ProfileID]