# app/crud/cart.py
from bson import ObjectId
from fastapi import HTTPException, status
from datetime import datetime
from db.connection import db
from schemas.cart import CartItemBase, Cart

collection = db["carts"]

def get_or_create_cart(user_id: str) -> dict:
    cart = collection.find_one({"user_id": user_id})
    if cart:
        return cart
    # create new cart doc
    doc = {
        "user_id": user_id,
        "created": datetime.utcnow().isoformat(),
        "items": []
    }
    collection.insert_one(doc)
    return collection.find_one({"user_id": user_id})

def list_cart(user_id: str) -> Cart:
    cart = get_or_create_cart(user_id)
    # convert each item _id to str
    items = [
        {**item, "id": str(item["_id"])}
        for item in cart["items"]
    ]
    return Cart(user_id=user_id, items=items, created=cart["created"])

def add_item(user_id: str, payload: CartItemBase) -> Cart:
    cart = get_or_create_cart(user_id)
    # try update existing item
    existing = next((it for it in cart["items"] if str(it["_id"]) == payload.product_id), None)
    # Actually compare on product_id
    existing = next((it for it in cart["items"] if str(it["product_id"]) == payload.product_id), None)
    if existing:
        # increment quantity
        collection.update_one(
            {"user_id": user_id, "items.product_id": ObjectId(payload.product_id)},
            {"$inc": {"items.$.quantity": payload.quantity}}
        )
    else:
        # push new subdocument with its own _id
        new_item = {
          "_id": ObjectId(),
          "product_id": ObjectId(payload.product_id),
          "quantity": payload.quantity
        }
        collection.update_one(
          {"user_id": user_id},
          {"$push": {"items": new_item}}
        )
    return list_cart(user_id)

def remove_item(user_id: str, item_id: str) -> None:
    result = collection.update_one(
        {"user_id": user_id},
        {"$pull": {"items": {"_id": ObjectId(item_id)}}}
    )
    # result.modified_count still 1 even if item not found, so verify via find
    cart = collection.find_one({"user_id": user_id})
    if any(str(it["_id"]) == item_id for it in cart["items"]):
        raise HTTPException(status_code=500, detail="Failed to remove item")
    # no return needed
