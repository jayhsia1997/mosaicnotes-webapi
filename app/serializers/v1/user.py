"""
User serializers
"""
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field

from app.libs.consts.enums import LoginMethod, Gender
from app.schemas.mixins import UUIDBaseModel


class APIUserLogin(BaseModel):
    """
    User login
    """
    login_method: LoginMethod = Field(default=LoginMethod.PASSWORD, serialization_alias="loginMethod", description="Login method")
    email: str = Field(..., description="Email", frozen=True)
    password: str = Field(..., description="Password", frozen=True)


class APILoginResponse(UUIDBaseModel):
    """
    Login response
    """
    sid: UUID = Field(..., serialization_alias="sid", description="Session ID")


# User register
class APIUserRegister(BaseModel):
    email: str = Field(
        min_length=5,
        max_length=64,
        description="Email",
        pattern=r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    )
    display_name: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=8)


class APIRegisterResponse(UUIDBaseModel):
    email: str = Field(description="Email")
    display_name: str = Field(description="Display name")


class APIUserInfo(UUIDBaseModel):
    """
    User info
    """
    model_config = {
        "use_enum_values": True,
    }
    email: str = Field(..., description="Email")
    display_name: str = Field(..., description="Display name")
    gender: Optional[Gender] = Field(..., description="Gender")
