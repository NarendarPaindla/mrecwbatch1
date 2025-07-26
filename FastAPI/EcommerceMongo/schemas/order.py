from pydantic import BaseModel, Field
from typing import List
from datetime import datetime

class OrderItemBase(BaseModel):
    product_id: str = Field(..., description="ID of the product")
    quantity:    int = Field(..., ge=1, description="Quantity ≥ 1")

class OrderItem(OrderItemBase):
    price_at_purchase: float  = Field(..., description="Snapshot price")
    id:                str    = Field(..., description="Item sub-doc ID")

    class Config:
        orm_mode = True

class OrderCreate(BaseModel):
    user_id: str                     = Field(..., description="ID of the user")
    items:   List[OrderItemBase]     = Field(..., min_items=1)

class Order(BaseModel):
    id:           str                = Field(..., description="Order ID")
    user_id:      str
    total_amount: float
    created:      datetime
    items:        List[OrderItem]

    class Config:
        orm_mode = True
