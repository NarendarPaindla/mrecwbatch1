from bson import ObjectId
from fastapi import HTTPException
from db.connection import db
from schemas.product import ProductCreate, Product

collection = db["products"]

def to_product(doc: dict) -> Product:
    """Convert Mongo document to Pydantic Product."""
    return Product(
        id=str(doc["_id"]),
        name=doc["name"],
        description=doc.get("description"),
        price=doc["price"]
    )

def create_product(payload: ProductCreate) -> Product:
    result = collection.insert_one(payload.dict())
    doc = collection.find_one({"_id": result.inserted_id})
    return to_product(doc)

def list_products() -> list[Product]:
    docs = collection.find()
    return [to_product(doc) for doc in docs]

def get_product_by_id(product_id: str) -> Product:
    try:
        oid = ObjectId(product_id)
    except Exception:
        raise HTTPException(400, "Invalid product ID")
    doc = collection.find_one({"_id": oid})
    if not doc:
        raise HTTPException(404, "Product not found")
    return to_product(doc)

def update_product(product_id: str, payload: ProductCreate) -> Product:
    try:
        oid = ObjectId(product_id)
    except Exception:
        raise HTTPException(400, "Invalid product ID")
    result = collection.update_one(
        {"_id": oid},
        {"$set": payload.dict()}
    )
    if result.matched_count == 0:
        raise HTTPException(404, "Product not found")
    doc = collection.find_one({"_id": oid})
    return to_product(doc)

def delete_product(product_id: str) -> None:
    try:
        oid = ObjectId(product_id)
    except Exception:
        raise HTTPException(400, "Invalid product ID")
    result = collection.delete_one({"_id": oid})
    if result.deleted_count == 0:
        raise HTTPException(404, "Product not found")
