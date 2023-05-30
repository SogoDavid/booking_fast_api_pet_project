import pytest
from httpx import AsyncClient


@pytest.mark.parametrize(
    "email, password, status_code",
    [
        ("kot@pes.com", "kotopes", 200),
        ("kot@pes.com", "kot0opes", 409),
        ("pes@pes.com", "kotopes", 200),
        ("abcde", "kotopes", 422),
    ],
)
async def test_register_user(
    email: str, password: str, status_code: int, ac: AsyncClient
):
    response = await ac.post(
        "/v1/auth/register",
        json={
            "email": email,
            "password": password,
        },
    )
    assert response.status_code == status_code


@pytest.mark.parametrize(
    "email, password, status_code",
    [
        ("test@test.com", "test", 200),
        ("david@example.com", "david", 200),
    ],
)
async def test_login_user(email: str, password: str, status_code: int, ac: AsyncClient):
    response = await ac.post(
        "/v1/auth/login",
        json={
            "email": email,
            "password": password,
        },
    )

    assert response.status_code == status_code
