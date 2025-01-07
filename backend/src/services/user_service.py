from pydantic import EmailStr

from src.models import User
from src.db.manager import BaseDbManager


class UserService:
    @staticmethod
    async def create(db_manager: BaseDbManager, user: User) -> None:
        await db_manager.create([user])
            
    @staticmethod
    async def get(db_manager: BaseDbManager, id: int) -> User:
        return await db_manager.get(User, id)
    
    @staticmethod
    async def get_by_username(db_manager: BaseDbManager, username: str) -> User:
        result = await db_manager.filter(User, (User.username == username,))
        return result.first()
    
    @staticmethod
    async def get_by_email(db_manager: BaseDbManager, email: EmailStr) -> User:
        result = await db_manager.filter(User, (User.email == email,))
        return result.first()
    
    @staticmethod
    async def delete(db_manager: BaseDbManager, user: User) -> None:
        await db_manager.delete(user)