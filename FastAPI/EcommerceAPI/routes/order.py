# app/routes/order.py
from fastapi import APIRouter, status, Depends
from schemas.order import OrderCreate, Order
from crud.order import place_order, get_order_by_id, list_orders
from typing import List

router = APIRouter(prefix="/orders", tags=["orders"])

# Mocked dependency
def get_current_user():
    return {"user_id": 1}

@router.post(
    "",
    response_model=Order,
    status_code=status.HTTP_201_CREATED
)
def api_place_order(
    payload: OrderCreate,
    user=Depends(get_current_user)
):
    payload.user_id = user["user_id"]
    return place_order(payload)

@router.get(
    "",
    response_model=List[Order]
)
def api_list_orders():
    return list_orders()

@router.get(
    "/{order_id}",
    response_model=Order
)
def api_get_order(order_id: int):
    return get_order_by_id(order_id)