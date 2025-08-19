"""
Handler for user-related operations
"""
import uuid
from datetime import datetime, timezone, timedelta

from starlette import status

from app import exceptions
from app.config import settings
from app.libs.consts.enums import LoginMethod
from app.libs.database import Session
from app.models import User, UserProfile, UserSession
from app.providers.password_provider import PasswordProvider
from app.schemas.user import UserBase, UserInfo, UserSecurity
from app.serializers.v1.user import UserLogin, LoginResponse, RegisterResponse, UserRegister


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

        return LoginResponse(id=user_security.id, sid=sid)

    async def register(self, model: UserRegister) -> RegisterResponse:
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

        return RegisterResponse(
            id=user_info.id,
            email=user_info.email,
            display_name=user_info.display_name
        )
