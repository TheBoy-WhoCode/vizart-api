from fastapi import APIRouter, status, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlalchemy.orm.session import Session
from ..database import get_db
from .. import models, oauth2
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
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"status": False, "detail": "Oops! I can't Validate you"})

    if token.user_id != current_user.id:
        return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content={"status": False, "detail": "Not authorized to perform requested action"})

    access_token = oauth2.create_access_token(
        data={"user_id": current_user.id})

    token_query.update({"access_token": access_token, "updated_at": datetime.now()},
                       synchronize_session=False)
    db.commit()
    return JSONResponse(status_code=status.HTTP_200_OK, content={"status": True, "detail": jsonable_encoder(token_query.first())})
