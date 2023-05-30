from sqlalchemy import insert

from app.bookings.models import Bookings
from app.DAO.base import BaseDAO
from app.database import async_session_maker
from app.hotels.models import Hotels
from app.hotels.rooms.models import Rooms
from app.users.models import Users


class ImporterDAO(BaseDAO):
    models = {
        "bookings": Bookings,
        "users": Users,
        "hotels": Hotels,
        "rooms": Rooms
    }

    @classmethod
    async def add_data(cls, table_name, data):
        async with async_session_maker() as session:
            query = insert(cls.models[table_name]).values(data)
            await session.execute(query)
            await session.commit()



