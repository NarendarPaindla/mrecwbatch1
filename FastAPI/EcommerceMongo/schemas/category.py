# app/schemas/category.py
from pydantic import BaseModel, Field
from typing import List, Optional
from schemas.product import Product

class CategoryBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)

class CategoryCreate(CategoryBase):
    pass

class Category(CategoryBase):
    id: str

    class Config:
        orm_mode = True

class ProductWithCategory(Product):
    category: Optional[Category] = None

    class Config:
        orm_mode = True
