from bson import ObjectId
from datetime import datetime
from fastapi import HTTPException, status
from db.connection import db
from schemas.order import OrderCreate, Order
from crud.product import collection as products_coll, to_product

orders_coll = db["orders"]

def place_order(payload: OrderCreate) -> Order:
    # 1. Validate & snapshot each product
    total = 0.0
    embedded_items = []
    for item in payload.items:
        try:
            pid = ObjectId(item.product_id)
        except Exception:
            raise HTTPException(status_code=400, detail="Invalid product ID")
        prod = products_coll.find_one({"_id": pid})
        if not prod:
            raise HTTPException(status_code=404, detail=f"Product {item.product_id} not found")
        price = prod["price"]
        total += price * item.quantity
        embedded_items.append({
            "_id": ObjectId(),
            "product_id": pid,
            "quantity": item.quantity,
            "price_at_purchase": price
        })

    # 2. Build order document
    doc = {
        "user_id": payload.user_id,
        "total_amount": total,
        "created": datetime.utcnow(),
        "items": embedded_items
    }
    result = orders_coll.insert_one(doc)
    oid = result.inserted_id

    return get_order_by_id(payload.user_id, str(oid))

def list_orders(user_id: str) -> list[Order]:
    docs = orders_coll.find({"user_id": user_id}).sort("created", -1)
    return [ _doc_to_order(doc) for doc in docs ]

def get_order_by_id(user_id: str, order_id: str) -> Order:
    try:
        oid = ObjectId(order_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid order ID")
    doc = orders_coll.find_one({"_id": oid, "user_id": user_id})
    if not doc:
        raise HTTPException(status_code=404, detail="Order not found")
    return _doc_to_order(doc)

def _doc_to_order(doc: dict) -> Order:
    # Convert embedded items
    items = []
    for it in doc["items"]:
        items.append({
            "id": str(it["_id"]),
            "product_id": str(it["product_id"]),
            "quantity": it["quantity"],
            "price_at_purchase": it["price_at_purchase"]
        })
    return Order(
        id=str(doc["_id"]),
        user_id=doc["user_id"],
        total_amount=doc["total_amount"],
        created=doc["created"],
        items=items
    )
