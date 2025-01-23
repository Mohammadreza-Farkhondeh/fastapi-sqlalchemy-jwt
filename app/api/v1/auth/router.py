from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.v1.auth.schemas import (
    SignupRequest,
    SignupResponse,
    TokenObtainRequest,
    TokenRefreshRequest,
    TokenResponse,
)
from app.core.security import JWTUtils
from app.dependencies import get_db
from app.services.user_service import UserService

router = APIRouter(tags=["auth"])


@router.post(
    "/signup", response_model=SignupResponse, status_code=status.HTTP_201_CREATED
)
def signup_user(signup_data: SignupRequest, db: Session = Depends(get_db)):
    """
    Endpoint for user registration.
    """
    user_service = UserService()
    try:
        user = user_service.create_user(db, signup_data)
        return SignupResponse(
            message="User registered successfully",
            user=user,
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/token/obtain", response_model=TokenResponse)
def obtain_token(token_request: TokenObtainRequest, db: Session = Depends(get_db)):
    """
    Endpoint for obtaining access and refresh tokens.
    """
    user_service = UserService()
    user = user_service.authenticate_user(
        db, email=token_request.email, password=token_request.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )

    access_token = JWTUtils.create_access_token({"sub": user.email})
    refresh_token = JWTUtils.create_refresh_token({"sub": user.email})
    return TokenResponse(
        access=access_token,
        refresh=refresh_token,
    )


@router.post("/token/refresh", response_model=TokenResponse)
def refresh_token(refresh_data: TokenRefreshRequest):
    """
    Endpoint for refreshing the access token.
    """
    payload = JWTUtils.verify_token(refresh_data.refresh)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token"
        )

    access_token = JWTUtils.create_access_token({"sub": payload["sub"]})
    return TokenResponse(
        access=access_token,
        refresh=refresh_data.refresh,
    )
