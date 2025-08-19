"""
Handler for user-related operations
"""
from app import exceptions
from app.libs.consts.enums import LoginMethod
from app.libs.database import Session
from app.serializers.v1.user import UserLogin, LoginResponse, RegisterResponse, UserRegister

from app.models.user import User
from app.libs.utils.security import hash_password, verify_password
from typing import Optional
from sqlalchemy import select

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
        if not model.email or not model.password:
            raise exceptions.BadRequestException(detail="Email and password are required")

        email = model.email.strip().lower()
        stmt = select(User).where(User.email == email)
        result = await self._session.execute(stmt)
        user: Optional[User] = result.scalar_one_or_none()

        if not user or not verify_password(model.password, user.password_hash):
            raise exceptions.UnauthorizedException(detail="Invalid username or password")

        return LoginResponse(id=str(user.id), username=user.username, message="Login successful")

    async def register(self, model: UserRegister) -> RegisterResponse:
        if not model.username or not model.password:
            raise exceptions.BadRequestException(detail="Username and password are required")

        
        stmt = select(User).where(User.username == model.username)
        result = await self._session.execute(stmt)
        if result.scalar_one_or_none():
            raise exceptions.ConflictException(detail="Username already exists")

       
        email = model.email.strip().lower() if model.email else None
        if email:
            stmt = select(User).where(User.email == email)
            result = await self._session.execute(stmt)
            if result.scalar_one_or_none():
                raise exceptions.ConflictException(detail="Email already registered")

        user = User(username=model.username, email=email, password_hash=hash_password(model.password))
        self._session.add(user)
        await self._session.commit()
        await self._session.refresh(user)

        return RegisterResponse(id=str(user.id), username=user.username)


       
