from typing import Optional
from fastapi.datastructures import UploadFile
from fastapi.params import File
from pydantic import BaseModel, EmailStr
from uuid import UUID


from app.database import Base

'''CREATE USER'''


class CreateUser(BaseModel):
    username: str
    email: EmailStr
    password: str
    number: str


'''TOKEN'''


class Token(BaseModel):
    access_token: str


'''TOKEN DATA'''


class TokenData(BaseModel):
    id: Optional[str] = None


'''OTP'''


class OTP(BaseModel):
    user_id: str
    otp: str


'''SEND OTP'''


class SendOTP(BaseModel):
    user_id: Optional[str]
    email: str
    number: Optional[int]


'''UPLOAD IMAGE'''


class UploadImage(BaseModel):
    id: UUID
    user_id: UUID


''' ADD PRODUCT'''


class AddProduct(BaseModel):
    product_name: str
    product_type: str
    product_desc: str
    product_price: float
    product_quantity: int
    category_name: str
    category_desc: str
