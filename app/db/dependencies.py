from app.db.connector import async_session
from app.db.user_dal import UserDal

# Asynchronously construct user dal object.
async def get_user_dal():
    async with async_session() as session:
        async with session.begin():
            yield UserDal(session)