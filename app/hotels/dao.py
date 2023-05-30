from datetime import date

from sqlalchemy import and_, func, or_, select

from app.bookings.models import Bookings
from app.DAO.base import BaseDAO
from app.database import async_session_maker
from app.hotels.models import Hotels
from app.hotels.rooms.models import Rooms


class HotelsDAO(BaseDAO):
    model = Hotels

    @classmethod
    async def find_all(cls, location: str, date_from: date, date_to: date):
        booked_rooms = (
            select(Bookings.room_id, func.count(Bookings.room_id).label("rooms_booked"))
            .select_from(Bookings)
            .where(
                or_(
                    and_(
                        Bookings.date_from >= date_from,
                        Bookings.date_from <= date_to,
                    ),
                    and_(
                        Bookings.date_from <= date_from,
                        Bookings.date_to > date_from,
                    ),
                ),
            )
            .group_by(Bookings.room_id)
            .cte("booked_rooms")
        )

        booked_hotels = (
            select(
                Rooms.hotel_id,
                func.sum(
                    Rooms.quantity - func.coalesce(booked_rooms.c.rooms_booked, 0)
                ).label("rooms_left"),
            )
            .select_from(Rooms)
            .join(booked_rooms, booked_rooms.c.room_id == Rooms.id, isouter=True)
            .group_by(Rooms.hotel_id)
            .cte("booked_hotels")
        )

        get_hotels_with_rooms = (
            select(
                Hotels.__table__.columns,
                booked_hotels.c.rooms_left,
            )
            .join(booked_hotels, booked_hotels.c.hotel_id == Hotels.id, isouter=True)
            .where(
                and_(
                    booked_hotels.c.rooms_left > 0,
                    Hotels.location.like(f"%{location}%"),
                )
            )
        )
        async with async_session_maker() as session:
            hotels_with_rooms = await session.execute(get_hotels_with_rooms)
            return hotels_with_rooms.mappings().all()
