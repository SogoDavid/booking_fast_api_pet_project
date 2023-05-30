from datetime import date, datetime, timedelta
from typing import List, Literal, Optional

from fastapi import APIRouter, Query

from app.exceptions import CannotBookHotelForLongPeriod, DateFromCannotBeAfterDateTo
from app.hotels.dao import HotelsDAO
from app.hotels.schemas import SHotel, SHotelInfo

router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get("/{location}")
async def get_all_hotels(
    location: Literal["Алтай", "Коми"],
    date_from: date = Query(..., example=datetime.now().date()),
    date_to: date = Query(..., example=(datetime.now() + timedelta(days=14)).date()),
) -> List[SHotelInfo]:
    if date_from > date_to:
        raise DateFromCannotBeAfterDateTo
    if (date_to - date_from).days > 30:
        raise CannotBookHotelForLongPeriod
    return await HotelsDAO.find_all(location, date_from, date_to)


@router.get("/id/{hotel_id}", include_in_schema=True)
async def get_hotel_by_id(
    hotel_id: int,
) -> Optional[SHotel]:
    return await HotelsDAO.find_one_or_none(id=hotel_id)
