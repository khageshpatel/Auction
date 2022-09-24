from typing import Any, List
from app.schemas.user import User

from fastapi import APIRouter

from app import schemas

router = APIRouter()


@router.get("/user_info", response_model=schemas.User)
def read_user(
) -> Any:
    """
    Retrieve user info.
    """
    return User(uuid="123", full_name="khagesh")