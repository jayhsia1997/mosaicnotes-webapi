"""
Util functions for lifespan
"""
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi_limiter import FastAPILimiter

from app.config import settings
from app.container import Container
from app.libs.database import RedisPool
from app.libs.logger import logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan
    :param app:
    """
    logger.info("Starting lifespan")
    # Create and wire container
    container = Container()
    # Register container with FastAPI
    app.container = container
    if settings.REDIS_URL:
        try:
            redis_connection = RedisPool().create(db=1)
            await FastAPILimiter.init(
                redis=redis_connection,
                prefix=f"{settings.APP_NAME}_limiter"
            )
            logger.info("FastAPILimiter initialized")
        except Exception as e:
            logger.error(f"Failed to initialize FastAPILimiter: {e}")
        else:
            yield
            await FastAPILimiter.close()
            await redis_connection.close()
        finally:
            logger.info("Lifespan finished")
    else:
        yield
