from pydantic import BaseModel

class ImageRegistration(BaseModel):
    id: str
    flag: int