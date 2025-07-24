# app/routes/cart.py
from fastapi import APIRouter, Depends, status
from crud.cart import add_item_to_cart, remove_item_from_cart, view_cart
from schemas.cart import CartItemCreate, Cart
from typing import Dict

router = APIRouter(prefix="/cart", tags=["cart"])

# Dummy “get current user” (mock)
def get_current_user() -> Dict[str,int]:
    # In real app: extract from JWT; here we hardcode
    return {"user_id": 1}

@router.post(
    "/items",
    response_model=CartItemCreate,
    status_code=status.HTTP_201_CREATED
)
def api_add_to_cart(
    payload: CartItemCreate,
    user=Depends(get_current_user)
):
    return add_item_to_cart(user["user_id"], payload)

@router.delete(
    "/items/{item_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def api_remove_from_cart(
    item_id: int,
    user=Depends(get_current_user)
):
    remove_item_from_cart(user["user_id"], item_id)

@router.get("", response_model=Cart)
def api_view_cart(user=Depends(get_current_user)):
    return view_cart(user["user_id"])