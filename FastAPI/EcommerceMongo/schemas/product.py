from pydantic import BaseModel,Field
from typing import Optional
class ProductBase(BaseModel):
     name:str=Field(...,min_length=1,description="Product name")
     description: Optional[str]=Field(None,description="Product description")
     price:float =Field(...,gt=0,description="Product price")
class ProductCreate(ProductBase):
    pass
class Product(ProductBase):
    id:str