from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr
from pydantic.types import conint


class CreateUser(BaseModel):
    username: str
    email: EmailStr
    password: str
    number : int
