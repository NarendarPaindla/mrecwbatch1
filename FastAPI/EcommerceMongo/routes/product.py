from fastapi import APIRouter, status
from typing import List
from crud.product import (
    create_product, list_products,
    get_product_by_id, update_product, delete_product
)
from schemas.product import Product, ProductCreate

router = APIRouter(prefix="/products", tags=["products"])

@router.post("", response_model=Product, status_code=status.HTTP_201_CREATED)
def api_create_product(payload: ProductCreate):
    return create_product(payload)

@router.get("", response_model=List[Product])
def api_list_products():
    return list_products()

@router.get("/{product_id}", response_model=Product)
def api_get_product(product_id: str):
    return get_product_by_id(product_id)

@router.put("/{product_id}", response_model=Product)
def api_update_product(product_id: str, payload: ProductCreate):
    return update_product(product_id, payload)

@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def api_delete_product(product_id: str):
    delete_product(product_id)
