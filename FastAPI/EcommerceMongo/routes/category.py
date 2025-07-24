from fastapi import APIRouter, status
from typing import List
from schemas.category import (
    CategoryCreate, Category, ProductWithCategory
)
from crud.category import (
    create_category, list_categories, get_category_by_id,
    update_category, delete_category, list_products_by_category
)

router = APIRouter(prefix="/categories", tags=["categories"])

@router.post(
    "",
    response_model=Category,
    status_code=status.HTTP_201_CREATED
)
def api_create_category(payload: CategoryCreate):
    return create_category(payload)

@router.get("", response_model=List[Category])
def api_list_categories():
    return list_categories()

@router.get("/{cat_id}", response_model=Category)
def api_get_category(cat_id: str):
    return get_category_by_id(cat_id)

@router.put("/{cat_id}", response_model=Category)
def api_update_category(cat_id: str, payload: CategoryCreate):
    return update_category(cat_id, payload)

@router.delete(
    "/{cat_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def api_delete_category(cat_id: str):
    delete_category(cat_id)

@router.get(
    "/{cat_id}/products",
    response_model=List[ProductWithCategory]
)
def api_list_products_by_category(cat_id: str):
    return list_products_by_category(cat_id)
