from fastapi import HTTPException, status


class BookingException(HTTPException):
    status = 500
    detail = ""

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class UserAlreadyExistException(BookingException):
    status_code = status.HTTP_409_CONFLICT
    detail = "Пользователь уже существует"


class IncorrectEmailOrPasswordException(BookingException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Неверная почта или пароль"


class TokenExpiredException(BookingException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Время жизни токена истекло"


class TokenAbsentException(BookingException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Токен не представлен"


class IncorrectTokenFormatException(BookingException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Неверный формат токена"


class RoomCannotBeBooked(BookingException):
    status_code = status.HTTP_409_CONFLICT
    detail = "Не осталось свободных номеров"


class RoomFullyBooked(BookingException):
    status_code = status.HTTP_409_CONFLICT
    detail = "Не осталось свободных номеров"


class DateFromCannotBeAfterDateTo(BookingException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Дата заселения не может быть раньше даты выселения"


class CannotBookHotelForLongPeriod(BookingException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Нельзя бронировать на период более 30 дней"

class OnlyAdminCanAddDataInDataBase(BookingException):
    status_code = status.HTTP_403_FORBIDDEN
    detail = "Только администратор может добавлять данные в базу данных напрямую"
