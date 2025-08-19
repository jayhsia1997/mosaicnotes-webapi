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
    username: str
    message: str | None = None


# User register
class UserRegister(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=8)
    email: str | None = None

class RegisterResponse(BaseModel):
    id: str
    username: str