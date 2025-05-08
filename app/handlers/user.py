"""
Handler for user-related operations
"""
from app import exceptions
from app.libs.consts.enums import LoginMethod
from app.libs.database import Session
from app.serializers.v1.user import UserLogin, LoginResponse


class UserHandler:
    """UserHandler"""

    def __init__(self, session: Session = None):
        """initialize"""
        self._session = session

    async def login(self, model: UserLogin) -> LoginResponse:
        """
        Login
        :param model:
        :return:
        """
        match model.login_method:
            case LoginMethod.PASSWORD:
                return await self.password_login(model=model)
            case _:
                raise exceptions.BadRequestException(detail="Invalid login method")

    async def password_login(self, model: UserLogin) -> LoginResponse:
        """
        Password login
        :param model:
        :return:
        """
        return LoginResponse()
