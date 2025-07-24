# app/crud/user.py
import bcrypt
from fastapi import HTTPException, status
from db.connection import get_db_connection
from schemas.user import UserCreate, User
from auth.jwt import create_access_token

def get_user_by_email(email: str) -> User | None:
    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM users WHERE email=%s;", (email,))
    row = cur.fetchone()
    cur.close(); conn.close()
    return User(**row) if row else None

def get_user_by_id(user_id: int) -> User:
    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM users WHERE id=%s;", (user_id,))
    row = cur.fetchone()
    cur.close(); conn.close()
    if not row:
        raise HTTPException(status_code=404, detail="User not found")
    return User(**row)

def create_user(user_in: UserCreate) -> User:
    if get_user_by_email(user_in.email):
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed = bcrypt.hashpw(user_in.password.encode(), bcrypt.gensalt()).decode()
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO users (email, hashed_password, role) VALUES (%s,%s,%s)",
        (user_in.email, hashed, "customer")
    )
    conn.commit()
    user_id = cur.lastrowid
    cur.close(); conn.close()
    return get_user_by_id(user_id)

def authenticate_user(email: str, password: str) -> User:
    user = get_user_by_email(email)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect credentials")
    if not bcrypt.checkpw(password.encode(), user.hashed_password.encode()):
        raise HTTPException(status_code=401, detail="Incorrect credentials")
    return user

def create_user_token(user: User) -> str:
    token_data = {"user_id": user.id, "role": user.role}
    return create_access_token(token_data)