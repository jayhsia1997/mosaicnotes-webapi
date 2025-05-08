"""
main application
"""
from fastapi import FastAPI, Request, status, HTTPException
from fastapi.exception_handlers import http_exception_handler
from fastapi.responses import JSONResponse, RedirectResponse
from starlette.middleware.cors import CORSMiddleware

from app.libs.utils.lifespan import lifespan
from app.config import settings
from app.routers import api_router
from app.container import Container

__all__ = ["app"]


def register_router(application: FastAPI) -> None:
    """
    register router
    :param application:
    :return:
    """
    application.include_router(api_router, prefix="/api")


def register_middleware(application: FastAPI) -> None:
    """
    register middleware
    :param application:
    :return:
    """
    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        allow_origin_regex=settings.CORS_ALLOW_ORIGINS_REGEX
    )


def get_application() -> FastAPI:
    """
    get application
    """
    application = FastAPI(
        lifespan=lifespan,
    )
    register_middleware(application=application)
    register_router(application=application)

    return application


app = get_application()


@app.get("/")
async def root():
    """
    Root path redirects to /docs in development environment
    """
    if settings.IS_DEV:
        return RedirectResponse(url="/docs")
    return {"message": "Welcome to MosaicNotes API"}


@app.exception_handler(HTTPException)
async def root_http_exception_handler(request, exc: HTTPException):
    """

    :param request:
    :param exc:
    :return:
    """
    return await http_exception_handler(request, exc)


@app.exception_handler(Exception)
async def exception_handler(request: Request, exc):
    """

    :param request:
    :param exc:
    :return:
    """
    content = {
        "detail": {
            "message": "Internal Server Error",
            "url": str(request.url)
        }
    }
    if settings.DEBUG:
        content["debug_detail"] = f"{exc.__class__.__name__}: {exc}"
    return JSONResponse(
        content=content,
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
    )
