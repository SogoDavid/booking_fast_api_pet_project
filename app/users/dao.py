from sqlalchemy import ClauseElement, insert

from app.DAO.base import BaseDAO
from app.database import async_session_maker
from app.users.models import Users


class UsersDAO(BaseDAO):
    model = Users

    @classmethod
    async def add_new_user(cls, **data):
        async with async_session_maker() as session:
            query: ClauseElement = insert(cls.model).values(data).returning(cls.model)
            result = await session.execute(query)
            await session.commit()
            inserted_user = result.scalar_one()
            return inserted_user
