import pytest
from httpx import AsyncClient


@pytest.mark.parametrize(
    "location, date_from, date_to, status_code",
    [
        ("Алтай", "2023-06-30", "2023-06-25", 400),
        ("Алтай", "2023-06-25", "2023-07-30", 400),
        ("Алтай", "2023-06-25", "2023-06-30", 200),
    ],
)
async def test_get_free_hotels(
    location: str, date_from: str, date_to: str, status_code: int, ac: AsyncClient
):
    response = await ac.get(
        f"/v1/hotels/{location}",
        params={
            "date_from": date_from,
            "date_to": date_to,
        },
    )
    print(response)
    assert response.status_code == status_code
