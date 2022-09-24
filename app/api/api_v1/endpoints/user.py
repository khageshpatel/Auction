from typing import Any, List
from app.schemas.product import Product
from app.schemas.user import User

from app.db.dependencies import get_user_dal
from app.db.user_dal import UserDal
from app.core.exception_handler import Handle
from fastapi import APIRouter, Depends, HTTPException

from app import schemas

router = APIRouter()


@router.get(
    "/user_info",
    response_model = schemas.User)
async def read_user(uuid: int, user_dal: UserDal = Depends(get_user_dal)) -> User:
    """
    Retrieve user info.
    """
    user = await user_dal.get_user(uuid)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.post("/user_create", response_model = schemas.User)
async def create_user(user: schemas.UserInfo, user_dal: UserDal = Depends(get_user_dal)) -> User:
    user = await user_dal.create_user(user)
    return user

@router.post("/product_create", response_model = schemas.Product)
async def create_product(product: schemas.Product, user_dal: UserDal = Depends(get_user_dal)) -> Product:
    try:
        await user_dal.create_product(product)
    except Exception as e:
        Handle(e)
    return product