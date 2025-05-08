"""
Demo serializers
"""
from typing import Optional

from pydantic import BaseModel, Field

from app.schemas.mixins import UUIDBaseModel
from app.serializers.mixins.base import PaginationBaseResponseModel


class DemoDetail(UUIDBaseModel):
    """
    Demo detail
    """
    name: str = Field(..., description="Name")
    remark: Optional[str] = Field(None, description="Remark")


class DemoList(BaseModel):
    """
    Demo list
    """
    items: Optional[list[DemoDetail]] = Field(..., description="Demo Items")


class DemoPages(PaginationBaseResponseModel):
    """
    Demo pages
    """
    items: Optional[list[DemoDetail]] = Field(..., description="Demo Items")
