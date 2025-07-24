# app/routes/auth.py
from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm

from schemas.user import UserCreate, User, Token
from crud.user import create_user, authenticate_user, create_user_token

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post(
    "/register",
    response_model=User,
    status_code=status.HTTP_201_CREATED
)
def register(user_in: UserCreate):
    return create_user(user_in)

@router.post(
    "/login",
    response_model=Token
)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    access_token = create_user_token(user)
    return {"access_token": access_token, "token_type": "bearer"}