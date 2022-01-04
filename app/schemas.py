from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr
from pydantic.types import conint

from app.database import Base

'''CREATE USER'''


class CreateUser(BaseModel):
    username: str
    email: EmailStr
    password: str
    number: int


'''TOKEN'''


class Token(BaseModel):
    access_token: str


'''TOKEN DATA'''


class TokenData(BaseModel):
    id: Optional[str] = None


'''OTP'''


class OTP(BaseModel):
    user_id: str
    otp: int


'''SEND OTP'''


class SendOTP(BaseModel):
    user_id: str
    email: str
    number: Optional[int]
