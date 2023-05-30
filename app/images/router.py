import shutil

from fastapi import APIRouter, Request, UploadFile
from jose import ExpiredSignatureError, jwt

from app.config import settings
from app.exceptions import OnlyAdminCanAddDataInDataBase, TokenExpiredException
from app.tasks.tasks import process_pic

router = APIRouter(prefix="/images", tags=["Загрузка картинок"])


@router.post("/hotels")
async def add_hotel_image(name: int,
                          file: UploadFile,
                          request: Request):
    """
    Только администратор может загружать картинки
    """
    try:
        decoded_token = jwt.decode(request.cookies.get("booking_access_token"), settings.SECRET_KEY)
        role = decoded_token["role"]
        if role != "admin":
            raise OnlyAdminCanAddDataInDataBase
    except ExpiredSignatureError:
        raise TokenExpiredException
    im_path = f"app/static/images/{name}.webp"
    with open(im_path, "wb+") as file_object:
        shutil.copyfileobj(file.file, file_object)
    process_pic.delay(im_path)
