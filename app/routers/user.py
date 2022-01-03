from enum import unique
from fastapi import status, HTTPException, APIRouter
from fastapi.param_functions import Form
from fastapi.params import Depends
from sqlalchemy.orm.session import Session
from sqlalchemy import exc
from starlette.status import HTTP_400_BAD_REQUEST
from ..database import get_db
from .. import models, schemas, utils
import uuid
import pyotp


router = APIRouter(
    prefix="/user",
    tags=["Register"]
)


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def create_user(user: schemas.CreateUser, db: Session = Depends(get_db)):

    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    if(len(str(user.number)) < 10):
        print("[INFO] inside number")
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST,
                            detail=f"Kidnly send a valid data")
    user_id = str(uuid.uuid1())
    new_user = models.Users(id=user_id, **user.dict())
    
    print(new_user)
    totp = pyotp.TOTP('base32secret3232', interval=120)
    otp = totp.now()

    
    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    except exc.IntegrityError:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"User email {user.email} already exist!")

    # user_query = db.query(models.Users).filter(models.Users.id == id).first()
    new_otp = models.OTP(id=str(uuid.uuid1()), user_id=user_id, )
    try:
        db.add()

    except:
        pass

    return {"user": new_user, "otp": otp}


@router.get("/{id}")
async def get_user(id: str, db: Session = Depends(get_db)):
    user = db.query(models.Users).filter(models.Users.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id {id} doesn't exist!")
    return user
