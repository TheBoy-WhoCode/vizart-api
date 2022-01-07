from uuid import uuid1
from fastapi import APIRouter, status, Depends
from fastapi.datastructures import UploadFile
from fastapi.encoders import jsonable_encoder
from fastapi.params import File, Form
from fastapi.responses import JSONResponse
from sqlalchemy.orm import query, query_expression
from sqlalchemy.orm.session import Session
from sqlalchemy.sql.functions import func, mode
from ..database import get_db
from .. import models
import os
import aiofiles


router = APIRouter(
    tags=['Product']
)


@router.post("/addProduct")
async def add_product(product_name: str = Form(...),
                      product_type: str = Form(...),
                      product_desc: str = Form(...),
                      product_price: float = Form(...),
                      product_quantity: int = Form(...),
                      category_name: str = Form(...),
                      category_desc: str = Form(...),
                      product_image: UploadFile = File(...), db: Session = Depends(get_db)):
    image_dir = "./products/"
    # print(product)
    product_id = uuid1()
    inventory_id = uuid1()
    category_id = uuid1()
    product_img_id = uuid1()
    try:
        if not os.path.isdir(image_dir):
            os.mkdir(image_dir)

        path = os.path.join(image_dir, str(
            product_img_id) + "-" + product_image.filename)
        async with aiofiles.open(path, "wb") as out_file:
            content = await product_image.read()
            await out_file.write(content)

        inventory = models.ProductInventory(
            id=inventory_id, quantity=product_quantity)

        category = models.ProductCategory(
            id=category_id,
            category_name=category_name,
            category_desc=category_desc)

        new_product = models.Products(
            id=product_id,
            inventory_id=inventory_id,
            category_id=category_id,
            product_name=product_name,
            product_type=product_type,
            price=product_price,

            product_desc=product_desc)

        prod_image = models.ProductImage(id=product_img_id,
                                         product_id=product_id,
                                         inventory_id=inventory_id,
                                         category_id=category_id,
                                         image_path=path)
        db.add(inventory)
        db.add(category)
        db.add(new_product)
        db.add(prod_image)
        db.commit()
    except Exception as e:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"status": False, "detail": f"Something wen't wrong {e}"})
    else:
        return JSONResponse(status_code=status.HTTP_200_OK, content={"status": False, "detail": f"Product Added Successfully."})


@router.get("/getProducts")
async def getProducts(db: Session = Depends(get_db)):
    try:

        query = db.query(models.Products,
                         models.ProductImage,
                         models.ProductCategory).filter(models.Products.id == models.ProductImage.product_id).filter(models.Products.category_id == models.ProductCategory.id).all()
    except Exception as e:
        print(e)
    else:
        return JSONResponse(status_code=status.HTTP_200_OK, content={"status": False, "detail": jsonable_encoder(query)})
    pass
