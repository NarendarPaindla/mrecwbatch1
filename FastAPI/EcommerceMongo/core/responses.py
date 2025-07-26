from pydantic import BaseModel
from typing import Any

class Success(BaseModel):
    success: bool = True
    data: Any

class Error(BaseModel):
    success: bool = False
    error: str
