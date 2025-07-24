# app/schemas/category.py
from pydantic import BaseModel

from schemas.product import Product

class CategoryBase(BaseModel):
    name: str

class CategoryCreate(CategoryBase):
    pass

class Category(CategoryBase):
    id: int

    class Config:
        orm_mode = True

# Extended response: product + category
class ProductWithCategory(Product):
    category: Category | None