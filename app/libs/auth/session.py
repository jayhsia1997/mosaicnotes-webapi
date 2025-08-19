"""
Session authentication dependencies
"""
from typing import Optional
from uuid import UUID

from dependency_injector.wiring import inject, Provide
from fastapi import Request, Depends
from fastapi.security import APIKeyCookie

from app import exceptions
from app.config import settings
from app.container import Container
from app.handlers import UserHandler
from app.libs.contexts.api_context import APIContext, set_api_context
from app.schemas.user import UserInfo


class SessionCookie(APIKeyCookie):
    """
    Custom cookie for session ID.
    """

    def __init__(self, name: str = settings.COOKIE_NAME, auto_error: bool = True):
        super().__init__(name=name, auto_error=auto_error)

    async def __call__(self, request: Request) -> APIContext:
        """
        Retrieve session ID from cookies.
        :param request: FastAPI request object
        :return: Session ID as UUID
        """
        cookie_value = request.cookies.get(self.model.name)
        if not cookie_value:
            raise exceptions.UnauthorizedException("Session not found")

        try:
            return await self.authenticate(request=request, session_id=UUID(cookie_value))
        except ValueError:
            raise exceptions.UnauthorizedException("Invalid session ID format")

    @inject
    async def authenticate(
        self,
        request: Request,
        session_id: UUID,
        user_handler: UserHandler = Provide[Container.user_handler]
    ) -> APIContext:
        """
        Authenticate session ID.
        :param request: FastAPI request object
        :param session_id: Session ID from cookies
        :param user_handler: User handler dependency
        :return: Session ID if valid
        """
        user: Optional[UserInfo] = await user_handler.get_user_by_session_id(session_id=session_id)
        if not user:
            raise exceptions.UnauthorizedException("Invalid session ID")
        api_context = APIContext(
            user_id=user.id,
            host=request.client.host,
            url=str(request.url),
            path=request.url.path
        )
        return api_context


async def session_validation(
    api_context: APIContext = Depends(SessionCookie()),
):
    """
    Validate session ID and retrieve user information.
    :param api_context: Session ID from cookies
    :return:
    """
    set_api_context(api_context)
    return api_context
