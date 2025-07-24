from pydantic import BaseModel,Field
from typing import Optional
class ProductBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100,
                      description="Product name, 1–100 chars")
    description: Optional[str] = Field(None, max_length=500,
                                       description="Optional, up to 500 chars")
    price: float = Field(..., gt=0,
                         description="Must be greater than 0")
class ProductCreate(ProductBase):
    pass
class Product(ProductBase):
    id:int