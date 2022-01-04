from fastapi import status, APIRouter
from fastapi.responses import JSONResponse
from fastapi.params import Depends
from sqlalchemy.orm.session import Session
from sqlalchemy import exc
from ..database import get_db
from .. import models, schemas, utils
import uuid
import pyotp


router = APIRouter(
    prefix="/user",
    tags=["User"]
)


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def create_user(user: schemas.CreateUser, db: Session = Depends(get_db)):

    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    if(len(str(user.number)) < 10):
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"status": False, "detail": "Kidnly send a valid data"})

    user_id = str(uuid.uuid1())
    totp = pyotp.TOTP('base32secret3232', interval=900)
    otp = totp.now()

    new_user = models.Users(id=user_id, **user.dict())
    new_otp = models.OTP(id=str(uuid.uuid1()), user_id=user_id, otp=otp)

    try:
        db.add(new_user)
        db.add(new_otp)

        db.commit()

        db.refresh(new_user)
        db.refresh(new_otp)

    except exc.IntegrityError:
        return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content={"status": False, "detail": f"User email {user.email} already exist!"})

    except exc:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"status": False, "detail": "Server issue"})

    return JSONResponse(status_code=status.HTTP_200_OK, content={"user": new_user, "otp": otp})


@router.get("/{id}", status_code=status.HTTP_200_OK)
async def get_user(id: str, db: Session = Depends(get_db)):
    user = db.query(models.Users).filter(models.Users.id == id).first()
    if not user:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"status": False, "detail": f"User with id {id} doesn't exist!"})

    return JSONResponse(status_code=status.HTTP_200_OK, content={"status": True, "detail": user})
