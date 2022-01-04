from fastapi import APIRouter, Response, status, Depends, HTTPException, File, UploadFile
from typing import List
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
import sqlalchemy
from sqlalchemy.orm.session import Session
from sqlalchemy.sql.functions import mode
from ..database import get_db
from .. import models, schemas, utils, oauth2
import uuid
from datetime import datetime
import os
import aiofiles
from fastapi.responses import JSONResponse

router = APIRouter(
    tags=['Trial Images']
)


@router.post("/uploadTrialImage")
async def upload_trial_image(files: List[UploadFile] = File(...), db: Session = Depends(get_db)):
    image_dir = "./trial_images/"
    try:
        if not os.path.isdir(image_dir):
            os.mkdir(image_dir)

        for file in files:
            file_id = uuid.uuid1()
            path = os.path.join(image_dir, str(
                file_id) + "-" + file.filename)
            async with aiofiles.open(path, "wb") as out_file:
                content = await file.read()
                await out_file.write(content)

            values = models.TrialImage(id=file_id, image_path=path)
            db.add(values)
            db.commit()
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST, content={
                "message": str(e)}
        )
    else:
        return JSONResponse(
            status_code=status.HTTP_200_OK, content={"status": True}
        )


@router.get("/trialImages")
async def get_trial_images(db: Session = Depends(get_db)):
    image_query = db.query(models.TrialImage).all()
    return image_query
