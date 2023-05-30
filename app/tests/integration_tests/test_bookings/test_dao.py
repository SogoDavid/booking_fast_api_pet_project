from datetime import datetime

from app.bookings.dao import BookingDAO
from app.bookings.models import Bookings


async def test_add_and_get_booking():
    new_booking: Bookings = await BookingDAO.add_str(
        user_id=2,
        room_id=2,
        date_from=datetime.strptime("2023-07-10", "%Y-%m-%d"),
        date_to=datetime.strptime("2023-07-20", "%Y-%m-%d"),
    )

    assert new_booking.user_id == 2
    assert new_booking.room_id == 2

    new_booking = await BookingDAO.find_by_id(new_booking.id)

    assert new_booking is not None


async def test_post_get_delete_get_booking():
    def validate_booking(response: Bookings):
        assert response.room_id == 2

    new_booking: Bookings = await BookingDAO.add_str(
        user_id=2,
        room_id=2,
        date_from=datetime.strptime("2023-07-10", "%Y-%m-%d"),
        date_to=datetime.strptime("2023-07-20", "%Y-%m-%d"),
    )
    validate_booking(new_booking)

    check_booking: Bookings = await BookingDAO.find_by_id(new_booking.id)
    validate_booking(check_booking)

    await BookingDAO.delete(id=new_booking.id)

    check_booking: Bookings = await BookingDAO.find_by_id(new_booking.id)
    assert check_booking is None
