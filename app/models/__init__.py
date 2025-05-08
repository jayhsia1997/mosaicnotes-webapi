"""
Top-level package for models.
"""
from app.config import settings
from .user import (
    User,
    UserProfile,
    UserSession,
)

__all__ = [
    "User",
    "UserProfile",
    "UserSession",
]

if settings.IS_DEV:
    from .demo import Demo

    __all__.append("Demo")
