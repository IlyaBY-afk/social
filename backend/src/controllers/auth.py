from fastapi import APIRouter
from passlib.context import CryptContext
import logging



router = APIRouter(prefix="/auth", tags=["users"])
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
logging.getLogger('passlib').setLevel(logging.ERROR)

fastapi