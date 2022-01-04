from datetime import datetime
from typing import Optional
from fastapi.datastructures import UploadFile
from fastapi.param_functions import File, Form
from pydantic import BaseModel, EmailStr
from pydantic.types import Json, conint
from uuid import UUID, uuid1
import json

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
    user_id: Optional[str]
    email: str
    number: Optional[int]


'''UPLOAD IMAGE'''


class UploadImage(BaseModel):
    id: UUID
    user_id: UUID

    # @classmethod
    # def __get_validators__(cls):
    #     yield cls.validate_to_json

    # @classmethod
    # def validate_to_json(cls, value):
    #     if isinstance(value, str):
    #         return cls(**json.loads(value))
    #     return value

    # def __init__(self, image: UploadFile = File(...)):
    #     id = uuid1()
    #     user_id = uuid1()
    #     super().__init__(id, user_id, image)
