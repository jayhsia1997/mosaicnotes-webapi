"""
Top level handlers package
"""
from app.config import settings
from .user import UserHandler

__all__ = [
    # user
    "UserHandler",
]

if settings.IS_DEV:
    from .demo import DemoHandler

    __all__.append("DemoHandler")
