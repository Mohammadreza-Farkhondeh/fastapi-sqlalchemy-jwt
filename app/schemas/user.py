from pydantic import BaseModel, EmailStr

from app.schemas.base import BaseSchema


class UserBase(BaseModel):
    username: str
    email: EmailStr


class UserCreate(UserBase):
    password: str


class UserUpdate(UserBase):
    password: str | None = None


class UserOut(UserBase, BaseSchema):
    is_active: bool
    is_superuser: bool
