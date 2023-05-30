from fastapi import APIRouter, Depends, Response

from app.exceptions import IncorrectEmailOrPasswordException, UserAlreadyExistException
from app.users.auth import auth_user, create_access_token, get_password_hash
from app.users.dao import UsersDAO
from app.users.dependencies import get_current_user
from app.users.models import Users
from app.users.schemas import SResponseUser, SuccessfulAuth, SuccessfulLogout, SUserAuth

router = APIRouter(prefix="/auth", tags=["Auth и Пользователи"])


@router.post("/register")
async def register_user(user_data: SUserAuth) -> SResponseUser:
    existing_user = await UsersDAO.find_one_or_none(email=user_data.email)
    if existing_user:
        raise UserAlreadyExistException
    else:
        hashed_password = get_password_hash(user_data.password)
        inserted_user = await UsersDAO.add_new_user(email=user_data.email, hashed_password=hashed_password)
        return SResponseUser(id=inserted_user.id, email=inserted_user.email)


@router.post("/login")
async def authenticate_user(response: Response, user_data: SUserAuth) -> SuccessfulAuth:
    user = await auth_user(user_data.email, user_data.password)
    if not user:
        raise IncorrectEmailOrPasswordException
    access_token = create_access_token({"sub": str(user.id), "email": str(user.email)})
    response.set_cookie(
        key="booking_access_token", value=access_token, httponly=True, samesite="strict"
    )
    return SuccessfulAuth(message=f"Аутентификация пользователя {user.email} прошла успешно",
            detail="Токен booking_access_token сохранен в сookies")


@router.post("/logout")
async def logout_user(response: Response) -> SuccessfulLogout:
    """
    Разлогинить пользователя (удаление токена из кук)

    Параметры:

    - Требуется кука `booking_access_token`.
    """
    response.delete_cookie("booking_access_token")
    return SuccessfulLogout(message="Ждем Вас снова:)", detail="Токен успешно удален из кук")


@router.get("/me", )
async def read_users_me(
        current_user: Users = Depends(get_current_user),
) -> SResponseUser:
    """
    Получение информации о текущем пользователе.

    Параметры:

    - Требуется кука `booking_access_token`.

    Возвращает:

    Информацию о текущем пользователе.

    Примечание:
    Для выполнения этого запроса необходимо отправить куку `booking_access_token` вместе с запросом.
    """
    return SResponseUser(id=current_user.id, email=current_user.email)
