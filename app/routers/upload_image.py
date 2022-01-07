import uuid
from fastapi import APIRouter, status, Depends
from fastapi.datastructures import UploadFile
from fastapi.encoders import jsonable_encoder
from fastapi.param_functions import File, Form
from fastapi.responses import JSONResponse
from sqlalchemy.orm import query
from sqlalchemy.orm.session import Session
from ..database import get_db
from .. import models, oauth2
import os
import aiofiles

from sqlalchemy.sql.expression import literal

router = APIRouter(
    tags=['Upload Image']
)


@router.post("/uploadImage")
async def upload_image(file: UploadFile = File(...), db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    image_dir = "./uploaded_images/"
    try:
        if not os.path.isdir(image_dir):
            os.mkdir(image_dir)
        file_id = uuid.uuid1()
        path = os.path.join(image_dir, str(file_id) + "-" + file.filename)
        async with aiofiles.open(path, "wb") as out_file:
            content = await file.read()
            await out_file.write(content)

        values = models.UploadImage(
            id=file_id, user_id=current_user.id, image_path=path)

        db.add(values)
        db.commit()
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST, content={"status":  False,
                                                              "detail": str(e)})
    else:
        return JSONResponse(
            status_code=status.HTTP_200_OK, content={
                "status": True, "msg": "success"})


@router.get("/getImages")
async def getUploadedImage(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    image_query = db.query(models.UploadImage).filter(
        models.UploadImage.user_id == current_user.id).all()
    return JSONResponse(
        status_code=status.HTTP_200_OK, content={
            "status": True, "detail": jsonable_encoder(image_query
                                                       )}
    )
