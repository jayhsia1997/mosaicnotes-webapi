"""
User schema.
"""
from typing import Optional

from pydantic import Field
from .mixins import UUIDBaseModel
from app.libs.consts.enums import Gender


class UserBase(UUIDBaseModel):
    """
    User base information.
    """
    email: str = Field(..., description="Email address")


class UserSecurity(UserBase):
    """
    User security information.
    """
    password_hash: str = Field(..., description="Password hash")
    salt: str = Field(..., description="Salt for password hashing")


class UserInfo(UserBase):
    """
    User information.
    """
    display_name: Optional[str] = Field(None, description="Display name")
    gender: Optional[Gender] = Field(None, description="Gender")
