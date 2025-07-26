from pydantic import BaseModel,Field
from typing import Optional
class ProductBase(BaseModel):
     name: str = Field(..., min_length=1, max_length=100,
                      description="1–100 chars")
     description: Optional[str] = Field(None, max_length=500)
     price: float = Field(..., gt=0, description="Must be > 0")
     stock: int   = Field(..., ge=0, description="Available stock (≥0)")
class ProductCreate(ProductBase):
    pass
class Product(ProductBase):
    id:str