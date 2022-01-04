from fastapi import APIRouter, status, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm.session import Session
from ..database import get_db
from .. import models, schemas
from datetime import datetime
import pyotp

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
    # join = db.query(models.Users).join(
    #     models.OTP, models.OTP.user_id == models.Users.id, isouter=True)
    print(temp.user_id)
    if not user:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"status": False, "detail": "User Not Found!"})

    totp = pyotp.TOTP('base32secret3232', interval=300)
    otp = totp.now()
    print(f"[INFO] {otp}")

    otp_query.update(
        {"otp": otp, "updated_at": datetime.utcnow()}, synchronize_session=False)
    db.commit()
    return JSONResponse(status_code=status.HTTP_200_OK, content={"status": True, "detail": "OTP sent successfully"})
