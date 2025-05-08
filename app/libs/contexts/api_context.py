"""
API Context
"""
from contextvars import ContextVar, Token
from typing import Optional
from uuid import UUID

from pydantic import BaseModel

auth_context = ContextVar("APIContext")


class APIContext(BaseModel):
    """API Context"""
    user_id: Optional[UUID] = None
    host: Optional[str] = None
    url: Optional[str] = None
    path: Optional[str] = None


def set_api_context(context: APIContext) -> Token:
    """

    :param context:
    :return:
    """
    return auth_context.set(context)


def get_api_context() -> APIContext:
    """

    :return:
    """
    return auth_context.get()
