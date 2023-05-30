from pydantic import BaseModel, EmailStr


class SUserAuth(BaseModel):
    email: EmailStr
    password: str


class SResponseUser(BaseModel):
    id: int
    email: EmailStr


class SuccessfulAuth(BaseModel):
    message: str
    detail: str

class SuccessfulLogout(BaseModel):
    message: str
    detail: str

