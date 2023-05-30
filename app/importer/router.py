import json
from datetime import datetime
from typing import Literal

from fastapi import APIRouter, Request, UploadFile
from jose import ExpiredSignatureError, jwt

from app.config import settings
from app.exceptions import OnlyAdminCanAddDataInDataBase, TokenExpiredException
from app.importer.dao import ImporterDAO

router = APIRouter(prefix="/importer", tags=["Добавление данных в таблицу"])

@router.post("/{table_name}",
             status_code=201,
             )
async def add_data_in_tables(table_name: Literal["bookings",
                                                 "hotels",
                                                 "rooms",
                                                 "users"],
                             file: UploadFile,
                             request: Request):
    """
    Ожидается формат `.json` от учетки администратора
    """
    data: json = json.loads(await file.read())
    if table_name == "bookings":
        for booking in data:
            booking["date_from"] = datetime.strptime(booking["date_from"], "%Y-%m-%d")
            booking["date_to"] = datetime.strptime(booking["date_to"], "%Y-%m-%d")
    try:
        decoded_token = jwt.decode(request.cookies.get("booking_access_token"), settings.SECRET_KEY)
        role = decoded_token["role"]
        if role != "admin":
            raise OnlyAdminCanAddDataInDataBase
    except ExpiredSignatureError:
        raise TokenExpiredException
    return await ImporterDAO.add_data(table_name, data)
