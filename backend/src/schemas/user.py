from fastapi import HTTPException
from pydantic import BaseModel, EmailStr, model_validator
from typing import Self


class UserRegisterSchema(BaseModel):
    email: EmailStr
    username: str
    password: str
    password_repeat: str

    @model_validator(mode='after')
    def confirm_password(self) -> Self:
        if self.password != self.password_repeat:
            raise HTTPException(status_code=400, detail="Passwords do not match.")
        return self
