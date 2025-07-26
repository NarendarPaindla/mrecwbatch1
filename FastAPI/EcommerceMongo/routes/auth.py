from fastapi import APIRouter, status
from schemas.user import UserCreate, User
from crud.user import create_user, authenticate_user

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post(
    "/register",
    response_model=User,
    status_code=status.HTTP_201_CREATED
)
def api_register(user_in: UserCreate):
    """
    Register a new user.
    """
    return create_user(user_in)

@router.post(
    "/login",
    response_model=User
)
def api_login(user_in: UserCreate):
    """
    Login with email & password.
    Returns user info on success.
    """
    return authenticate_user(user_in.email, user_in.password)
