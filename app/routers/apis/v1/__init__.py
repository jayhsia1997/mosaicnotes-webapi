"""
Top level router for v1 API
"""
from fastapi import APIRouter

from app.config import settings
from .user import router as user_router

router = APIRouter()
router.include_router(user_router, prefix="/user", tags=["User"])

if settings.IS_DEV:
    from .demo import router as demo_router

    router.include_router(demo_router, prefix="/demo", tags=["Demo"])
