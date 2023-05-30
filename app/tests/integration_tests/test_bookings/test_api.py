import pytest
from httpx import AsyncClient


@pytest.mark.parametrize(
    "room_id, date_from, date_to, booked_rooms, status_code",
    [
        *[(4, "2030-05-01", "2030-05-15", i, 201) for i in range(3, 10)],
        *[
            (4, "2030-05-01", "2030-05-15", 10, 201)
            if i == 0
            else (4, "2030-05-01", "2030-05-15", 10, 409)
            for i in range(3)
        ],
    ],
)
async def test_add_and_get_booking(
    room_id: int,
    date_from: str,
    date_to: str,
    booked_rooms: int,
    status_code: int,
    authenticated_ac: AsyncClient,
):
    response = await authenticated_ac.post(
        "/v1/bookings",
        json={"room_id": 4, "date_from": "2030-05-01", "date_to": "2030-05-15"},
    )
    assert response.status_code == status_code
    assert response.json()

    response = await authenticated_ac.get("/v1/bookings")
    assert len(response.json()) == booked_rooms


async def test_get_and_delete_bookings(authenticated_ac: AsyncClient):
    response = await authenticated_ac.get("/v1/bookings")
    for booking in response.json():
        await authenticated_ac.delete(f"/v1/bookings/{booking['id']}")
    response = await authenticated_ac.get("/v1/bookings")
    assert not response.json()
