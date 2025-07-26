from pydantic import BaseModel, EmailStr, Field

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str = Field(..., min_length=8, description="At least 8 characters")

class User(UserBase):
    id: str

    class Config:
        orm_mode = True
