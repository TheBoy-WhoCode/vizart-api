from fastapi import APIRouter, status, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm.session import Session
from ..database import get_db
from .. import models, schemas

router = APIRouter(
    prefix="/product",
    tags=['Product']
)


@router.post("/addProduct")
async def add_product(db: Session = Depends(get_db)):
    pass
