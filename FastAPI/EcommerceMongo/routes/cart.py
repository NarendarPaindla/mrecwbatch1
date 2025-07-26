# app/routes/cart.py
from fastapi import APIRouter, status
from typing import List
from crud.cart import list_cart, add_item, remove_item
from schemas.cart import Cart, CartItemBase

router = APIRouter(prefix="/carts", tags=["cart"])

@router.get("/{user_id}", response_model=Cart)
def api_list_cart(user_id: str):
    """
    View or create the cart for `user_id`.
    """
    return list_cart(user_id)

@router.post(
    "/{user_id}/items",
    response_model=Cart,
    status_code=status.HTTP_201_CREATED
)
def api_add_item(user_id: str, payload: CartItemBase):
    """
    Add a product (by product_id) to the cart, or increment its quantity.
    """
    return add_item(user_id, payload)

@router.delete(
    "/{user_id}/items/{item_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def api_remove_item(user_id: str, item_id: str):
    """
    Remove an item (by its sub-document ID) from the cart.
    """
    remove_item(user_id, item_id)
