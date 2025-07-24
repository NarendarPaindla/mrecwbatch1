# app/auth/deps.py

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import JWTError  # ✅ Corrected import

from auth.jwt import verify_access_token
from schemas.user import TokenData
from crud.user import get_user_by_id

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = verify_access_token(token)
        user_id: int = payload.get("user_id")
        role: str = payload.get("role")

        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token payload")

        token_data = TokenData(user_id=user_id, role=role)

    except JWTError:  # ✅ Correct exception used
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = get_user_by_id(token_data.user_id)
    return user


def get_current_active_user(current_user=Depends(get_current_user)):
    # You can add more checks here, e.g., if current_user.is_active
    return current_user


def get_current_admin(current_user=Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return current_user
