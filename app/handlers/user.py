"""
Handler for user-related operations
"""
import uuid
from datetime import datetime, timezone, timedelta
from typing import Optional, Any, Coroutine

from starlette import status

from app import exceptions
from app.config import settings
from app.libs.consts.enums import LoginMethod
from app.libs.contexts.api_context import get_api_context, APIContext
from app.libs.database import Session
from app.models import User, UserProfile, UserSession
from app.providers.password_provider import PasswordProvider
from app.schemas.user import UserBase, UserInfo, UserSecurity
from app.serializers.v1.user import APIUserLogin, APILoginResponse, APIRegisterResponse, APIUserRegister, APIUserInfo


class UserHandler:
    """UserHandler"""

    def __init__(
        self,
        password_provider: PasswordProvider = None,
        session: Session = None
    ):
        """initialize"""
        self._password_provider = password_provider
        self._session = session
        try:
            self._api_context: APIContext = get_api_context()
        except Exception:
            self._api_context: APIContext = APIContext()

    async def login(self, model: APIUserLogin) -> APILoginResponse:
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

    async def password_login(self, model: APIUserLogin) -> APILoginResponse:
        """
        Password login
        :param model:
        :return:
        """
        user_security: UserBase = await self._session.select(User).where(
            User.email == model.email.strip().lower()
        ).fetchrow(UserSecurity)

        if not user_security or not self._password_provider.verify_password(
            password=model.password,
            password_hash=user_security.password_hash,
            salt=user_security.salt
        ):
            raise exceptions.UnauthorizedException(detail="Invalid username or password")

        try:
            # Generate session ID
            sid = uuid.uuid4()
            # Store session in database or cache (not implemented here)
            user_info: UserInfo = await self._session.select(
                User.id.label("id"),
                User.email.label("email"),
                UserProfile.display_name.label("display_name")
            ).outerjoin(
                UserProfile, UserProfile.user_id == User.id
            ).where(User.id == user_security.id).fetchrow(UserInfo)

            expired_at = datetime.now(tz=timezone.utc) + timedelta(seconds=settings.SESSION_TTL)
            await self._session.insert(UserSession).values(
                id=sid,
                user_id=user_security.id,
                data=user_info.model_dump_json(),
                expired_at=expired_at
            ).execute()
        except Exception as e:
            await self._session.rollback()
            raise exceptions.ApiBaseException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to create session: {str(e)}"
            )
        else:
            await self._session.commit()
        finally:
            await self._session.close()

        return APILoginResponse(id=user_security.id, sid=sid)

    async def logout(self):
        """
        # TODO: Implement logout functionality
        :return:
        """

    async def register(self, model: APIUserRegister) -> APIRegisterResponse:
        user_base = self._session.select(User).where(User.email == model.email).fetch(UserBase)
        if not user_base:
            raise exceptions.ResourceExistsException(detail="Email already registered")

        try:
            user_id = uuid.uuid4()
            password_hash, salt = self._password_provider.hash_password(password=model.password)
            await self._session.insert(User).values(
                id=user_id,
                email=model.email.strip().lower(),
                password_hash=password_hash,
                salt=salt,
            ).execute()
            await self._session.insert(UserProfile).values(
                user_id=user_id,
                display_name=model.display_name.strip(),
            ).execute()
            user_info: UserInfo = await self._session.select(
                User.id.label("id"),
                User.email.label("email"),
                UserProfile.display_name.label("display_name")
            ).outerjoin(
                UserProfile, UserProfile.user_id == User.id
            ).where(User.id == str(user_id)).fetchrow(UserInfo)
        except Exception as e:
            await self._session.rollback()
            raise exceptions.ApiBaseException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to register user: {str(e)}"
            )
        else:
            await self._session.commit()
        finally:
            await self._session.close()

        return APIRegisterResponse(
            id=user_info.id,
            email=user_info.email,
            display_name=user_info.display_name
        )

    async def get_me(self) -> APIUserInfo:
        """
        Get current user information
        :return: UserInfo or None
        """
        return await self.get_user_by_id(user_id=self._api_context.user_id)

    async def get_user_by_id(self, user_id: uuid.UUID) -> APIUserInfo:
        """
        Get user by ID
        :param user_id: User ID
        :return: UserInfo or None
        """
        user_info: UserInfo = await self._session.select(
            User.id,
            User.email,
            UserProfile.display_name,
            UserProfile.gender
        ).outerjoin(
            UserProfile, UserProfile.user_id == User.id
        ).where(User.id == user_id).fetchrow(UserInfo)
        if not user_info:
            raise exceptions.NotFoundException(detail="User not found")

        return APIUserInfo(
            id=user_info.id,
            email=user_info.email,
            display_name=user_info.display_name,
            gender=user_info.gender
        )

    async def get_user_by_session_id(self, session_id: uuid.UUID) -> Optional[UserInfo]:
        """
        Get user by session ID
        :param session_id: Session ID
        :return: UserInfo or None
        """
        user_id = await self._session.select(UserSession.user_id).where(
            UserSession.id == session_id
        ).fetchval()

        if not user_id:
            return None

        user_info: UserInfo = await self._session.select(
            User.id.label("id"),
            User.email.label("email"),
            UserProfile.display_name.label("display_name")
        ).outerjoin(
            UserProfile, UserProfile.user_id == User.id
        ).where(User.id == user_id).fetchrow(UserInfo)
        return user_info
