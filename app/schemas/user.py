from typing import Optional

from pydantic import BaseModel, EmailStr

from app.schemas.base import BaseSchema


class UserBase(BaseModel):
    username: str
    email: EmailStr


class UserCreate(UserBase):
    password: Optional[str] = None
    hashed_password: Optional[str] = None


class UserUpdate(UserBase):
    password: str | None = None


class UserOut(UserBase, BaseSchema):
    is_active: bool
    is_superuser: bool
