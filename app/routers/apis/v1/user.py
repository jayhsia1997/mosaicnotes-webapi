"""
Account API Router
"""
from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, Response, Request
from starlette import status

from app.config import settings
from app.container import Container
from app.handlers import UserHandler
from app.route_classes import LogRoute
from app.serializers.v1.user import UserLogin, LoginResponse, UserRegister, RegisterResponse

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
    response: Response,
    user_handler: UserHandler = Depends(Provide[Container.user_handler]),
) -> LoginResponse:
    """
    Login
    :param model:
    :param response:
    :param user_handler:
    :return:
    """
    res: LoginResponse = await user_handler.login(model=model)
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
    response_model=RegisterResponse,
    status_code=status.HTTP_201_CREATED
)
@inject
async def register(
    model: UserRegister,
    user_handler: UserHandler = Depends(Provide[Container.user_handler]),
) -> RegisterResponse:
    """
    Register a new user.
    :param model:
    :param user_handler:
    :return:
    """
    return await user_handler.register(model=model)


@router.get("/me", status_code=status.HTTP_200_OK)
async def me(user_handler: UserHandler = Depends(Provide[Container.user_handler])):
    """
    Get current user information.
    # TODO
    :param user_handler:
    :return:
    """


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout(request: Request, response: Response):
    """
    Logout user by deleting the session cookie.
    # TODO
    :param request:
    :param response:
    :return:
    """
