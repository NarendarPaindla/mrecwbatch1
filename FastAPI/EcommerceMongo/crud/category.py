from typing import List
from bson import ObjectId
from fastapi import HTTPException, status
from db.connection import db
from schemas.category import CategoryCreate, Category, ProductWithCategory
from crud.product import to_product

collection = db["categories"]
products_coll = db["products"]

def create_category(payload: CategoryCreate) -> Category:
    result = collection.insert_one(payload.dict())
    doc = collection.find_one({"_id": result.inserted_id})
    return Category(id=str(doc["_id"]), name=doc["name"])

def list_categories() -> List[Category]:
    docs = collection.find()
    return [Category(id=str(d["_id"]), name=d["name"]) for d in docs]

def get_category_by_id(cat_id: str) -> Category:
    try:
        oid = ObjectId(cat_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid category ID")
    doc = collection.find_one({"_id": oid})
    if not doc:
        raise HTTPException(status_code=404, detail="Category not found")
    return Category(id=cat_id, name=doc["name"])

def update_category(cat_id: str, payload: CategoryCreate) -> Category:
    try:
        oid = ObjectId(cat_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid category ID")
    result = collection.update_one({"_id": oid}, {"$set": payload.dict()})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Category not found")
    return get_category_by_id(cat_id)

def delete_category(cat_id: str) -> None:
    try:
        oid = ObjectId(cat_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid category ID")
    # Prevent deleting if products exist
    if products_coll.count_documents({"category_id": oid}) > 0:
        raise HTTPException(
            status_code=400,
            detail="Cannot delete category while products reference it"
        )
    result = collection.delete_one({"_id": oid})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Category not found")

def list_products_by_category(cat_id: str) -> List[ProductWithCategory]:
    try:
        oid = ObjectId(cat_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid category ID")
    cat_doc = collection.find_one({"_id": oid})
    if not cat_doc:
        raise HTTPException(status_code=404, detail="Category not found")
    cat_model = Category(id=cat_id, name=cat_doc["name"])
    prod_docs = products_coll.find({"category_id": oid})
    results: List[ProductWithCategory] = []
    for doc in prod_docs:
        p = to_product(doc)
        results.append(ProductWithCategory(**p.dict(), category=cat_model))
    return results
