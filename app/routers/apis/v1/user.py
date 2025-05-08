"""
Account API Router
"""
from fastapi import APIRouter, Depends
from starlette import status
from dependency_injector.wiring import inject, Provide

from app.container import Container
from app.handlers import UserHandler
from app.route_classes import LogRoute
from app.serializers.v1.user import UserLogin, LoginResponse

router = APIRouter(
    route_class=LogRoute
)


@router.post(
    path="/login",
    response_model=LoginResponse,
    status_code=status.HTTP_200_OK
)
@inject
async def login(
    model: UserLogin,
    user_handler: UserHandler = Depends(Provide[Container.user_handler])
) -> LoginResponse:
    """
    Login
    :param model:
    :param user_handler:
    :return:
    """
    return await user_handler.login(model=model)
