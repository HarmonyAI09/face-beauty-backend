from datetime import timedelta
from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm

from ...db.models.user_model import User
from ...api.dependencies.auth import get_current_user
from ...db.schemas.user_schema import UserRead, UserCreate, UserLogin, UserUpdate
from ...services.user_service import get_users, create_user, authenticate_user, update_user_info
from ...core.jwt_handler import ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token

router = APIRouter()

@router.post("/signup", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def signup_user(user: UserCreate):
    return await create_user(user)

@router.post("/signin", response_model=UserRead)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"}
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub":user.email}, expires_delta=access_token_expires
    )
    return {"access_token":access_token, "token_type": "bearer"}

@router.get("/users", response_model=list[UserRead])
async def read_users():
    return await get_users()

@router.put("/users/{user_id}", response_model=UserRead)
async def update_user(user_id: str, user_update: UserUpdate, current_user: User = Depends(get_current_user)):
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Not authorize to update this user's information")
    update_user = await update_user_info(user_id, user_update.dict(exclude_unset=True))
    return update_user