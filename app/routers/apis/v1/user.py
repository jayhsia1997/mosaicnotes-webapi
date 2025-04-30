"""
Account API Router
"""
from fastapi import APIRouter
from starlette import status

from app.libs.depends import (
    DEFAULT_RATE_LIMITERS,
)
from app.route_classes import LogRoute
from app.serializers.v1.user import UserLogin, LoginResponse
from app.handlers import UserHandler

router = APIRouter(
    dependencies=[
        *DEFAULT_RATE_LIMITERS
    ],
    route_class=LogRoute
)


@router.post(
    path="/login",
    response_model=LoginResponse,
    status_code=status.HTTP_200_OK
)
async def login(
    model: UserLogin,
) -> LoginResponse:
    """
    Login
    """
    user_handler = UserHandler()
    return await user_handler.login(model=model)
