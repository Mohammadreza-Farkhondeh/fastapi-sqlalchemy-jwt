from fastapi import APIRouter

from app.api.v1.auth.router import router as auth_router

v1_router = APIRouter()

v1_router.include_router(auth_router, prefix="/auth", tags=["auth"])
