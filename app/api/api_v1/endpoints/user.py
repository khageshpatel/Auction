from typing import Any, List
from app.schemas.user import User

from app.db.dependencies import get_user_dal
from app.db.user_dal import UserDal

from fastapi import APIRouter, Depends

from app import schemas

router = APIRouter()


@router.get(
    "/user_info",
    response_model = schemas.User)
async def read_user(uuid: 'str', user_dal: UserDal = Depends(get_user_dal)) -> User:
    """
    Retrieve user info.
    """
    return await user_dal.get_user(uuid)