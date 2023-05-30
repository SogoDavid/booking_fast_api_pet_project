from typing import List

from fastapi import APIRouter, Depends
from fastapi_versioning import version
from pydantic import parse_obj_as

from app.bookings.dao import BookingDAO
from app.bookings.schemas import SBooking, SNewBooking
from app.exceptions import RoomCannotBeBooked
from app.tasks.tasks import send_booking_confirmation_email
from app.users.dependencies import get_current_user
from app.users.models import Users

router = APIRouter(
    prefix="/bookings",
    tags=["Бронирования"],
)


@router.get("")
@version(1)
async def get_bookings(
    user: Users = Depends(get_current_user),
) -> List[SBooking]:
    return await BookingDAO.find_all(user_id=user.id)


@router.post("", status_code=201)
@version(1)
async def add_booking(
    booking: SNewBooking,
    user: Users = Depends(get_current_user),
) -> SBooking:
    booking = await BookingDAO.add_str(
        user.id,
        booking.room_id,
        booking.date_from,
        booking.date_to,
    )
    booking_dict = parse_obj_as(SNewBooking, booking).dict()
    send_booking_confirmation_email.delay(booking_dict, user.email)
    if not booking:
        raise RoomCannotBeBooked
    return booking


@router.delete("/{booking_id}", status_code=204)
@version(1)
async def delete_booking(booking_id: int, user: Users = Depends(get_current_user)):
    await BookingDAO.delete(id=booking_id, user_id=user.id)
