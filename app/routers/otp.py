from fastapi import APIRouter, Response, status, Depends, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy import schema
from sqlalchemy.orm.session import Session
from ..database import get_db
from .. import models, schemas, utils, oauth2

router = APIRouter(
    prefix="/api/otp",
    tags=['OTP']
)

@router.post("/")
async def OTP():
    pass