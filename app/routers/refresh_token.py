from fastapi import APIRouter, Response, status, Depends, HTTPException
from fastapi.param_functions import Form
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy import schema
from sqlalchemy.orm.session import Session
from ..database import get_db
from .. import models, schemas, utils, oauth2
from datetime import datetime


router = APIRouter(
    tags=['Refresh Token']
)


@router.post("/refreshToken")
async def refreshToken(access_token: str, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    print(current_user.id)
    token_query = db.query(models.Tokens).filter(
        models.Tokens.user_id == current_user.id)

    token = token_query.first()
    if not token:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Oops! I can't Validate you")
    if token.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")
    access_token = oauth2.create_access_token(
        data={"user_id": current_user.id})
    # values = models.Tokens(id=token.id,
    #                        user_id=current_user.id, access_token=access_token)
    token_query.update({"access_token": access_token, "updated_at": datetime.now()},
                       synchronize_session=False)
    db.commit()
    return token_query.first()
