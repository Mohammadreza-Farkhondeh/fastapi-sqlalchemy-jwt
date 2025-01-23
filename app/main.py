from fastapi import FastAPI

from app.api import api_router
from app.api.middleware.logging import LoggingMiddleware
from app.core.config import settings
from app.core.logging import setup_logging

setup_logging()
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.API_VERSION,
    description="Project description goes here",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_tags=[
        {"name": "auth", "description": "Authentication and user management"},
        {"name": "projects", "description": "Project-related operations"},
        {"name": "inference", "description": "Model inference endpoints"},
    ],
)


app.add_middleware(LoggingMiddleware)


app.include_router(api_router)


@app.get("/health", tags=["system"])
async def health_check():
    """
    Basic health check endpoint.
    """
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
