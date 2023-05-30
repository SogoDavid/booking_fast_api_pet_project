from sqlalchemy import ClauseElement, delete, insert, select
from sqlalchemy.ext.asyncio import AsyncResult

from app.database import async_session_maker


class BaseDAO:
    model = None

    @classmethod
    async def find_by_id(cls, model_id: int):
        async with async_session_maker() as session:
            query: ClauseElement = select(cls.model).filter_by(id=model_id)
            result: AsyncResult = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def find_one_or_none(cls, **filter_by):
        async with async_session_maker() as session:
            query: ClauseElement = select(cls.model).filter_by(**filter_by)
            result: AsyncResult = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def find_all(cls, **filter_by):
        async with async_session_maker() as session:
            query: ClauseElement = select(cls.model).filter_by(**filter_by)
            result: AsyncResult = await session.execute(query)
            return result.scalars().all()

    @classmethod
    async def add_str(cls, **data):
        async with async_session_maker() as session:
            query: ClauseElement = insert(cls.model).values(data)
            await session.execute(query)
            await session.commit()

    @classmethod
    async def delete(cls, **filter_by):
        async with async_session_maker() as session:
            query = delete(cls.model).filter_by(**filter_by)
            await session.execute(query)
            await session.commit()
