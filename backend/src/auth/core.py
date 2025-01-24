import uuid
import re
from typing import Optional

from fastapi import Depends, Request
from fastapi_users import BaseUserManager, UUIDIDMixin, models
from fastapi_users.authentication import (
    JWTStrategy,
)
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from fastapi_users.exceptions import InvalidPasswordException
from src.schemas.user import UserCreate

from src.models import User
from src.db.config import get_user_db


SECRET = "SECRET"


class UserManager(UUIDIDMixin, BaseUserManager[User, uuid.UUID]):
    reset_password_token_secret = SECRET
    verification_token_secret = SECRET

    async def validate_password(self, password: str, user: UserCreate | User) -> None:
        if len(password) < 8:
            raise InvalidPasswordException(
                reason="The password must be at least 8 characters long."
            )
        if re.match("^(.{0,7}|[^0-9]*|[^A-Z]*|[^a-z]*|[a-zA-Z0-9]*)$", password) is not None:
            raise InvalidPasswordException(
                reason="The password must contain at least one uppercase and one lowercase letter, one digit and one special character."
            )


    async def on_after_register(self, user: User, request: Optional[Request] = None):
        print(f"User {user.id} has registered.")

    async def on_after_forgot_password(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        print(f"User {user.id} has forgot their password. Reset token: {token}")

    async def on_after_request_verify(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        print(f"Verification requested for user {user.id}. Verification token: {token}")


async def get_user_manager(user_db: SQLAlchemyUserDatabase = Depends(get_user_db)):
    yield UserManager(user_db)


def get_jwt_strategy() -> JWTStrategy[models.UP, models.ID]:
    return JWTStrategy(secret=SECRET, lifetime_seconds=3600)
