"""
Top level router for v1 API
"""
from fastapi import APIRouter
from .user import router as user_router

router = APIRouter()
router.include_router(user_router, prefix="/user", tags=["User"])
