from math import prod
from sqlalchemy.orm import Session
from app.models.user import User
from app.models.product import Product
from app import schemas

class UserDal():
    def __init__(self, db_session: Session) -> None:
        self.db_session = db_session
    
    async def get_user(self, user_id : int) -> User:
        return await self.db_session.get(User, user_id)
    
    async def create_user(self, user_info : schemas.UserInfo) -> User:
        user = User(full_name = user_info.full_name)
        self.db_session.add(user)
        await self.db_session.flush()
        await self.db_session.refresh(user)
        return user
    
    async def create_product(self, request : schemas.Product) -> None:
        product = await self.db_session.get(Product, request.product_id)
        if product:
            product.full_name = request.full_name
            product.user_id = request.user_id
        else:
            product = Product(product_id = request.product_id, full_name = request.full_name, user_id = request.user_id)
            self.db_session.add(product)
        await self.db_session.flush()
