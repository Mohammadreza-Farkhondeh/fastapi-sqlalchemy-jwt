from typing import Any, Dict, Optional

from fastapi import HTTPException, status


class BaseAPIException(HTTPException):
    """
    Base custom exception for standardized API error responses.
    """

    def __init__(
        self, detail: Any = None, status_code: int = status.HTTP_400_BAD_REQUEST
    ):
        super().__init__(status_code=status_code, detail=detail)


class StandardResponse:
    """
    Utility class to create standardized API responses.
    """

    @staticmethod
    def success(
        data: Optional[Any] = None,
        message: str = "Success",
        status_code: int = status.HTTP_200_OK,
    ) -> Dict[str, Any]:
        return {"status": "success", "message": message, "data": data}

    @staticmethod
    def error(
        message: str, status_code: int = status.HTTP_400_BAD_REQUEST
    ) -> Dict[str, Any]:
        return {"status": "error", "message": message}
