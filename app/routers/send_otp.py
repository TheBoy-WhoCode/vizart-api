from fastapi import APIRouter, Response, status, Depends, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm.session import Session
from ..database import get_db
from .. import models, schemas, utils, oauth2
import uuid
from datetime import datetime
import pyotp

router = APIRouter(
    tags=['Send OTP']
)


@router.post("/sendOTP",  status_code=status.HTTP_200_OK)
async def sendOTP(data: schemas.SendOTP, db: Session = Depends(get_db)):
    user_query = db.query(models.Users).filter(models.Users.id == data.user_id)
    otp_query = db.query(models.OTP).filter(models.OTP.user_id == data.user_id)
    user = user_query.first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={
                            "status": False, "detail": "User Not Found!"})
    totp = pyotp.TOTP('base32secret3232', interval=300)
    otp = totp.now()
    print(f"[INFO] {otp}")

    otp_query.update(
        {"otp": otp, "updated_at": datetime.utcnow()}, synchronize_session=False)
    db.commit()
    return {"status": True, "detail": "OTP sent successfully"}
