from fastapi import APIRouter, Query, status
from typing import List, Optional
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
def api_list_products(
    page: int = Query(1, ge=1, description="Page number, starting at 1"),
    size: int = Query(10, ge=1, le=100, description="Items per page"),
    search: Optional[str] = Query(None, description="Filter by name or description"),
    sort: Optional[str] = Query(
        None,
        regex="^price_(asc|desc)$",
        description="Sort by price: 'price_asc' or 'price_desc'"
    )
):
    """
    List products with optional pagination, search, and sorting.
    """
    return list_products(page=page, size=size, search=search, sort=sort)

@router.get("/{product_id}", response_model=Product)
def api_get_product(product_id: str):
    return get_product_by_id(product_id)

@router.put("/{product_id}", response_model=Product)
def api_update_product(product_id: str, payload: ProductCreate):
    return update_product(product_id, payload)

@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def api_delete_product(product_id: str):
    delete_product(product_id)
