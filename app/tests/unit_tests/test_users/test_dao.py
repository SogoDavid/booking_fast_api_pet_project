import pytest

from app.users.dao import UsersDAO
from app.users.models import Users


@pytest.mark.parametrize(
    "user_id, email, exist",
    [
        (1, "test@test.com", True),
        (2, "david@example.com", True),
        (3, "tweqqwem", False),
    ],
)
async def test_find_by_id(user_id: int, email: str, exist: bool):
    user: Users = await UsersDAO.find_by_id(user_id)

    if exist:
        assert user
        assert user.id == user_id
        assert user.email == email
    else:
        print(user)
