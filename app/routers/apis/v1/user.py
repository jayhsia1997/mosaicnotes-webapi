"""
Account API Router
"""
from fastapi import APIRouter, Depends, Response, Request
from starlette import status
from dependency_injector.wiring import inject, Provide

from app.container import Container
from app.handlers import UserHandler
from app.route_classes import LogRoute
from app.serializers.v1.user import UserLogin, LoginResponse, UserRegister, RegisterResponse

from app.libs.deps.auth import get_current_user, get_session_store
from app.libs.session_store import SessionStore



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
    store: SessionStore = Depends(get_session_store),
) -> LoginResponse:
    """
    Login
    :param model:
    :param user_handler:
    :return:
    """

    res = await user_handler.login(model=model)
    sid = await store.create({"uid": res.id, "username": res.username}, ttl=SESSION_TTL)
    response.set_cookie(
        key=COOKIE_NAME,
        value=sid,
        httponly=True,
        secure=True,      
        samesite="lax",   
        path="/",
        max_age=SESSION_TTL,
    )
    return res

@router.post("/register", response_model=RegisterResponse, status_code=status.HTTP_201_CREATED)
@inject
async def register(
    model: UserRegister,
    user_handler: UserHandler = Depends(Provide[Container.user_handler]),
) -> RegisterResponse:
    return await user_handler.register(model=model)

@router.get("/me", status_code=status.HTTP_200_OK)
async def me(user = Depends(get_current_user)):
    return user 

@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout(request: Request, response: Response, store: SessionStore = Depends(get_session_store)):
    sid = request.cookies.get(COOKIE_NAME)
    if sid:
        await store.delete(sid)
    response.delete_cookie(key=COOKIE_NAME, path="/")