from pydantic import BaseModel, Field

from app.schemas.user import UserCreate, UserOut


class SignupRequest(UserCreate):
    """
    Schema for user registration requests.
    Inherits from UserCreate to avoid redundancy.
    """

    password: str = Field(..., min_length=8, example="strongpassword123")


class SignupResponse(BaseModel):
    """
    Schema for user registration responses.
    """

    message: str = Field(default="User registered successfully")
    user: UserOut


class TokenObtainRequest(BaseModel):
    """
    Schema for obtaining tokens (login).
    """

    email: str = Field(..., example="m@example.com")
    password: str = Field(..., example="securepassword123")


class TokenResponse(BaseModel):
    """
    Schema for token responses (both obtain and refresh).
    """

    access: str
    refresh: str


class TokenRefreshRequest(BaseModel):
    """
    Schema for refreshing tokens.
    """

    refresh: str
