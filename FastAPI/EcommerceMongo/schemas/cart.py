
from pydantic import BaseModel, Field
from typing import List, Optional

class CartItemBase(BaseModel):
    product_id: str = Field(..., description="ID of the product")
    quantity: int    = Field(..., ge=1, description="Quantity ≥ 1")

class CartItem(CartItemBase):
    id: str          = Field(..., description="Item sub-document ID")

    class Config:
        orm_mode = True

class Cart(BaseModel):
    user_id: str
    items: List[CartItem] = []
    created: Optional[str]  # ISO datetime

    class Config:
        orm_mode = True
