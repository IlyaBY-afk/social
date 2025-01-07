from fastapi import Depends, HTTPException, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from passlib.context import CryptContext
import logging

from src.auth import get_current_user, create_access_token
from src.models import User
from src.services.user_service import UserService
from src.db.config import db_manager
from src.schemas.user import UserRegisterSchema


router = APIRouter(prefix="/auth", tags=["users"])
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
logging.getLogger('passlib').setLevel(logging.ERROR)


@router.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await UserService.get_by_username(db_manager, form_data.username)
    if user is None or not pwd_context.verify(form_data.password, user.password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/register")
async def register(data: UserRegisterSchema):
    user = await UserService.get_by_username(db_manager, data.username)
    if user:
        raise HTTPException(status_code=422, detail="Username already exists.")
    user = await UserService.get_by_email(db_manager, data.username)
    if user:
        raise HTTPException(status_code=422, detail="Email already exists.")
    
    new_user = User.model_validate(data)
    new_user.password = pwd_context.hash(new_user.password)
    await UserService.create(db_manager, new_user)

    return {"201", "User registered successfully."}


@router.get("/protected")
async def protected_route(username: str = Depends(get_current_user)):
    return {"message": f"Hello, {username}! This is a protected resource."}