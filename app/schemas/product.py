from typing import Optional

from pydantic import BaseModel


# Shared properties
class Product(BaseModel):
    user_id: int
    product_id: str
    full_name: Optional[str] = None

    class Config:
        orm_mode = True