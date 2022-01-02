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

# '''REFRESH TOKEN'''


# class RefreshToken(BaseModel):
#     id: str
#     access_token: str
