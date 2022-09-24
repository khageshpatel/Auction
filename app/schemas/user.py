from typing import Optional

from pydantic import BaseModel


# Shared properties
class UserBase(BaseModel):
    full_name: Optional[str] = None

class UserInfo(UserBase):
    pass

# User DB Schema
class UserInDBBase(UserBase):
    user_id: int

    class Config:
        orm_mode = True

# User info and any additional info we will return via API.
class User(UserInDBBase):
    pass