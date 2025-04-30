"""
Exception for APIs
"""
from typing import Any, Optional, Dict

from fastapi import HTTPException
from starlette import status


class ApiBaseException(HTTPException):
    """API Base Exception"""

    def __init__(
        self,
        status_code: int,
        detail: Any = None,
        headers: Optional[Dict[str, Any]] = None,
        **kwargs
    ):
        super().__init__(
            status_code=status_code,
            detail=detail,
            headers=headers
        )
        self.debug_detail = kwargs.pop('debug_detail', None)

    def __str__(self):
        return self.detail or ""


class BadRequestException(ApiBaseException):
    """
    Bad Request Exception
    status_code: 400
    """

    def __init__(
        self,
        detail: str,
        headers: Optional[Dict[str, Any]] = None,
        **kwargs
    ):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail, headers=headers)
        self.debug_detail = kwargs.pop('debug_detail', None)


class NotFoundException(ApiBaseException):
    """
    Not Found Exception
    status_code: 404
    """

    def __init__(
        self,
        detail: str,
        headers: Optional[Dict[str, Any]] = None,
        **kwargs
    ):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail, headers=headers)
        self.debug_detail = kwargs.pop('debug_detail', None)


class ResourceExistsException(ApiBaseException):
    """
    Resource Exists Exception
    status_code: 409
    """

    def __init__(
        self,
        detail: str,
        headers: Optional[Dict[str, Any]] = None,
        **kwargs
    ):
        super().__init__(status_code=status.HTTP_409_CONFLICT, detail=detail, headers=headers)
        self.debug_detail = kwargs.pop('debug_detail', None)


class NotImplementedException(ApiBaseException):
    """
    Not Implemented Exception
    status_code: 501
    """

    def __init__(
        self,
        detail: str,
        headers: Optional[Dict[str, Any]] = None,
        **kwargs
    ):
        super().__init__(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail=detail, headers=headers)
        self.debug_detail = kwargs.pop('debug_detail', None)
