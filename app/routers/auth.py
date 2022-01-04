from fastapi import APIRouter, Response, status, Depends, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy import schema
from sqlalchemy.orm.session import Session
from ..database import get_db
from .. import models, schemas, utils, oauth2
import uuid
from datetime import datetime

router = APIRouter(
    tags=['Authentication']
)


@router.post("/login",  status_code=status.HTTP_200_OK)
async def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.Users).filter(
        models.Users.email == user_credentials.username).first()
    token_query = db.query(models.Tokens).filter(
        models.Tokens.user_id == user.id)
    token = token_query.first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")

    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")

    access_token = oauth2.create_access_token(data={"user_id": user.id})
    values = models.Tokens(id=str(uuid.uuid1()),
                           user_id=user.id, access_token=access_token)

    if token is None:
        print("[INFO] Inside IF")
        db.add(values)
        db.commit()
        db.refresh(values)
    else:
        print("[INFO] Inside Else")
        token_query.update({"access_token": access_token, "updated_at": datetime.now()},
                           synchronize_session=False)
        db.commit()

    return_value = {"access_token": access_token, "status": "success"}
    return return_value
