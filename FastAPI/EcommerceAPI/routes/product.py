from fastapi import APIRouter,status
from schemas.product import Product,ProductCreate
from crud.product import create_product
router=APIRouter(prefix="/products",tags=["products"])

@router.post("",response_model=Product,status_code=status.HTTP_201_CREATED)
def api_create_product(payload:ProductCreate):
    return create_product(payload)