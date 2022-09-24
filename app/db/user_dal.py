from sqlalchemy.orm import Session
from app.models.user import User

class UserDal():
    def __init__(self, db_session: Session) -> None:
        self.db_session = db_session
    
    async def get_user(self, uuid : str) -> User:
        return await self.db_session.get(User, uuid)