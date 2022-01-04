from fastapi import APIRouter, status, Depends, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from sqlalchemy.orm.session import Session
from sqlalchemy.sql.sqltypes import JSON
from ..database import get_db
from .. import models, utils, oauth2
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

    if user.status == False:
        return JSONResponse(status_code=status.HTTP_200_OK, content={"status": False, "detail": f"User not verified yet!"})

    if not user:
        return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content={"status": False, "detail": f"Invalid Credentials"})

    if not utils.verify(user_credentials.password, user.password):
        return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content={"status": False, "detail": f"Invalid Credentials"})

    access_token = oauth2.create_access_token(data={"user_id": user.id})
    values = models.Tokens(id=str(uuid.uuid1()),
                           user_id=user.id, access_token=access_token)

    if token is None:
        db.add(values)
        db.commit()
        db.refresh(values)
    else:
        token_query.update({"access_token": access_token, "updated_at": datetime.now()},
                           synchronize_session=False)
        db.commit()

    return JSONResponse(status_code=status.HTTP_200_OK, content={"status": True, "access_token": access_token})
