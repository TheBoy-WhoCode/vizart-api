from fastapi import APIRouter, status, Depends, HTTPException
from fastapi.datastructures import UploadFile
from fastapi.param_functions import File, Form
from fastapi.responses import JSONResponse
from sqlalchemy.orm.session import Session
from ..database import get_db
from .. import models, schemas, oauth2

router = APIRouter(
    prefix="/uploadImage",
    tags=['Upload Image']
)


@router.post("/")
async def upload_image(data: schemas.UploadImage, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    print(data.user_id)
