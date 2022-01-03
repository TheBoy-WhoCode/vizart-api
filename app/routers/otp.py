from fastapi import APIRouter, Response, status, Depends, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy import exc
from sqlalchemy.orm.session import Session
from sqlalchemy.sql.functions import mode
from ..database import get_db
from .. import models, schemas, utils, oauth2

router = APIRouter(
    tags=['OTP']
)


@router.post("/otp", status_code=status.HTTP_200_OK)
async def OTP(otp: schemas.OTP, db: Session = Depends(get_db)):
    otp_query = db.query(models.OTP).filter(
        models.OTP.user_id == otp.user_id).first()

    if not otp_query:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id {id} doesn't exist!")
    if otp.otp == otp_query.otp:
        user_query = db.query(models.Users).filter(
            models.Users.id == otp.user_id)
        user_query.update({"status": True}, synchronize_session=False)
        db.commit()
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f"Unable to verify OTP!")

    return {"status": "User verified Successfully!"}
