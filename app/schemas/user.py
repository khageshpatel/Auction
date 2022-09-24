from typing import Optional

from pydantic import BaseModel


# Shared properties
class UserBase(BaseModel):
    uuid: str
    full_name: Optional[str] = None

# User DB Schema
class UserInDBBase(UserBase):

    class Config:
        orm_mode = True

# User info and any additional info we will return via API.
class User(UserInDBBase):
    pass