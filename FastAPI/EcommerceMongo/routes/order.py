from fastapi import APIRouter, status
from typing import List
from schemas.order import OrderCreate, Order
from crud.order import place_order, list_orders, get_order_by_id

router = APIRouter(prefix="/orders", tags=["orders"])

@router.post(
    "",
    response_model=Order,
    status_code=status.HTTP_201_CREATED
)
def api_place_order(payload: OrderCreate):
    """
    Place a new order for a user.
    """
    return place_order(payload)

@router.get(
    "/{user_id}",
    response_model=List[Order]
)
def api_list_orders(user_id: str):
    """
    List all orders for a given user_id.
    """
    return list_orders(user_id)

@router.get(
    "/{user_id}/{order_id}",
    response_model=Order
)
def api_get_order(user_id: str, order_id: str):
    """
    Get a single order by ID for a user.
    """
    return get_order_by_id(user_id, order_id)
