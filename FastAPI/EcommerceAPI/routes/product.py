from fastapi import APIRouter,status
from schemas.product import Product,ProductCreate
from crud.product import (create_product, delete_product,list_products, update_product)
router=APIRouter(prefix="/products",tags=["products"])

@router.post("",response_model=Product,status_code=status.HTTP_201_CREATED)
def api_create_product(payload:ProductCreate):
    return create_product(payload)

@router.get("",response_model=list[Product])
def api_list_products():
    return list_products()

@router.put("/{product_id}", response_model=Product)
def api_update_product(product_id: int, payload: ProductCreate):
    return update_product(product_id, payload)

@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def api_delete_product(product_id: int):
    delete_product(product_id)