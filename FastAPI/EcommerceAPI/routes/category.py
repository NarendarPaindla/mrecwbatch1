# app/routes/category.py
from fastapi import APIRouter, status
from crud.category import (
    create_category, list_categories,
    get_category, list_products_by_category
)
from schemas.category import Category, CategoryCreate

router = APIRouter(prefix="/categories", tags=["categories"])

@router.post("", response_model=Category, status_code=status.HTTP_201_CREATED)
def api_create_category(payload: CategoryCreate):
    return create_category(payload)

@router.get("", response_model=list[Category])
def api_list_categories():
    return list_categories()

@router.get("/{cat_id}", response_model=Category)
def api_get_category(cat_id: int):
    return get_category(cat_id)

@router.get("/{cat_id}/products")
def api_list_products_by_category(cat_id: int):
    return list_products_by_category(cat_id)