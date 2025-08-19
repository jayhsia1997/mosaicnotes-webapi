"""
Account API Router
"""
from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, Response, Request
from starlette import status

from app.config import settings
from app.container import Container
from app.handlers import UserHandler
from app.libs.auth import session_validation
from app.route_classes import LogRoute
from app.serializers.v1.user import APIUserLogin, APILoginResponse, APIUserRegister, APIRegisterResponse, APIUserInfo

router = APIRouter(
    route_class=LogRoute
)


@router.post(
    path="/login",
    response_model=APILoginResponse,
    status_code=status.HTTP_200_OK
)
@inject
async def login(
    model: APIUserLogin,
    response: Response,
    user_handler: UserHandler = Depends(Provide[Container.user_handler]),
) -> APILoginResponse:
    """
    Login
    :param model:
    :param response:
    :param user_handler:
    :return:
    """
    res: APILoginResponse = await user_handler.login(model=model)
    response.set_cookie(
        key=settings.COOKIE_NAME,
        value=res.sid.hex,
        httponly=True,
        secure=True,
        samesite="strict",
        path="/",
        max_age=settings.SESSION_TTL,
    )
    return res


@router.post(
    "/register",
    response_model=APIRegisterResponse,
    status_code=status.HTTP_201_CREATED
)
@inject
async def register(
    model: APIUserRegister,
    user_handler: UserHandler = Depends(Provide[Container.user_handler]),
) -> APIRegisterResponse:
    """
    Register a new user.
    :param model:
    :param user_handler:
    :return:
    """
    return await user_handler.register(model=model)


@router.get(
    "/me",
    response_model=APIUserInfo,
    status_code=status.HTTP_200_OK,
    dependencies=[
        Depends(session_validation)
    ]
)
@inject
async def me(user_handler: UserHandler = Depends(Provide[Container.user_handler])) -> APIUserInfo:
    """
    Get current user information.
    :param user_handler:
    :return:
    """
    return await user_handler.get_me()


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
@inject
async def logout(
    request: Request,
    response: Response,
    user_handler: UserHandler = Depends(Provide[Container.user_handler])
):
    """
    Logout user by deleting the session cookie.
    :param request:
    :param response:
    :param user_handler:
    :return:
    """
    await user_handler.logout()
    # TODO: Implement logout logic in UserHandler
