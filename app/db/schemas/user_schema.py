from pydantic import BaseModel, EmailStr

class UserRead(BaseModel):
    id: int
    name: str
    email: str

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserUpdate(BaseModel):
    level: int

class SubScription(BaseModel):
    customer_id: str
    payment_method_id: str
    price_id: str

class CreateCustomer(BaseModel):
    email: EmailStr

class PremiumUser(BaseModel):
    email: EmailStr