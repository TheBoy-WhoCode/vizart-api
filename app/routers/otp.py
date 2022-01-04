from os import stat_result
from fastapi import APIRouter, status, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm.session import Session
from ..database import get_db
from .. import models, schemas

router = APIRouter(
    tags=['OTP']
)


@router.post("/otp", status_code=status.HTTP_200_OK)
async def OTP(otp: schemas.OTP, db: Session = Depends(get_db)):
    otp_query = db.query(models.OTP).filter(
        models.OTP.user_id == otp.user_id).first()

    if not otp_query:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"status": False, "detail": f"User with id {id} doesn't exist!"})

    if otp.otp == otp_query.otp:
        user_query = db.query(models.Users).filter(
            models.Users.id == otp.user_id)
        user_query.update({"status": True}, synchronize_session=False)
        db.commit()
    else:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"status": False, "detail": "Unable to verify OTP!"})

    return JSONResponse(status_code=status.HTTP_200_OK, content={"status": True, "details": "User verified Successfully!"})
