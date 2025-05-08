"""
Root router.
"""
from fastapi import APIRouter

from .apis.v1 import router as api_v1_router
from app.libs.depends import DEFAULT_RATE_LIMITERS
from app.config import settings

if settings.REDIS_URL:
    router = APIRouter(
        dependencies=[*DEFAULT_RATE_LIMITERS]
    )
else:
    router = APIRouter()
router.include_router(api_v1_router, prefix="/v1")


@router.get(
    path="/healthcheck"
)
async def healthcheck():
    """
    Healthcheck endpoint
    :return:
    """
    return {
        "message": "ok"
    }
