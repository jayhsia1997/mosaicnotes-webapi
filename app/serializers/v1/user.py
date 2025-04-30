"""
User serializers
"""
from pydantic import BaseModel, Field

from app.libs.consts.enums import LoginMethod
from app.schemas.mixins import UUIDBaseModel


class UserLogin(BaseModel):
    """
    User login
    """
    login_method: LoginMethod = Field(
        serialization_alias="loginMethod",
        description="Login method"
    )
    email: str = Field(
        ...,
        description="Email",
        frozen=True
    )
    password: str = Field(
        ...,
        description="Password",
        frozen=True
    )


class LoginResponse(UUIDBaseModel):
    """
    Login response
    """
