from fastapi import APIRouter, status, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlalchemy.orm.session import Session
from ..database import get_db
from .. import models, schemas
from datetime import datetime
import pyotp
import uuid

router = APIRouter(
    tags=['Send OTP']
)


@router.post("/sendOTP",  status_code=status.HTTP_200_OK)
async def sendOTP(data: schemas.SendOTP, db: Session = Depends(get_db)):
    user_query = db.query(models.Users).filter(
        models.Users.email == data.email)

    user = user_query.first()
    otp_query = db.query(models.OTP).filter(models.OTP.user_id == user.id)
    temp = otp_query.first()

    if temp is None:
        totp = pyotp.TOTP('base32secret3232', interval=300)
        otp = totp.now()
        otp_model = models.OTP(id=str(uuid.uuid1()), user_id=user.id, otp=otp)
        db.add(otp_model)
        db.commit()
    elif user.id == temp.user_id:
        totp = pyotp.TOTP('base32secret3232', interval=300)
        otp = totp.now()

        otp_query.update(
            {"otp": otp, "updated_at": datetime.utcnow()}, synchronize_session=False)
        db.commit()

    if not user:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"status": False, "detail": "User Not Found!"})

    return JSONResponse(status_code=status.HTTP_200_OK, content={"status": True, "detail": {"msg": "OTP sent successfully", "user_id": jsonable_encoder(user.id)}})
