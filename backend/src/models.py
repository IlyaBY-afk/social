from sqlalchemy.ext.declarative import declarative_base
from sqlmodel import SQLModel, Field, String
from pydantic import EmailStr
from datetime import datetime


AlchemyBase = declarative_base()
SQLModel.metadata = AlchemyBase.metadata


class Base(SQLModel, table=False):
    id: int = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now())


class User(Base, table=True):
    __tablename__ = 'users'

    email: EmailStr = Field(
        sa_type=String(),
        unique=True,
        index=True,
        nullable=False
    )
    username: str = Field(index=True)
    password: str = Field()
