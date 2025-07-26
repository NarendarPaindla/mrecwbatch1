from pymongo.errors import DuplicateKeyError
from bson import ObjectId
from fastapi import HTTPException, status
import bcrypt
from datetime import datetime

from db.connection import db
from schemas.user import UserCreate, User

users_coll = db["users"]
# Ensure unique index on email
users_coll.create_index("email", unique=True)

def create_user(payload: UserCreate) -> User:
    hashed = bcrypt.hashpw(payload.password.encode(), bcrypt.gensalt()).decode()
    doc = {
        "email": payload.email,
        "hashed_password": hashed,
        "created": datetime.utcnow()
    }
    try:
        res = users_coll.insert_one(doc)
    except DuplicateKeyError:
        raise HTTPException(status_code=400, detail="Email already registered")
    return User(id=str(res.inserted_id), email=payload.email)

def authenticate_user(email: str, password: str) -> User:
    doc = users_coll.find_one({"email": email})
    if not doc:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    if not bcrypt.checkpw(password.encode(), doc["hashed_password"].encode()):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    return User(id=str(doc["_id"]), email=doc["email"])
