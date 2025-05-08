"""
Dependency injection container for the application.
"""
from dependency_injector import containers, providers

from app.config import settings
from app.handlers import UserHandler
from app.libs.database import Session
from app.libs.database.aio_pg import PostgresConnection

if settings.IS_DEV:
    from app.handlers import DemoHandler


class Container(containers.DeclarativeContainer):
    """
    Dependency injection container for the application.
    """
    # Wire packages
    wiring_config = containers.WiringConfiguration(
        modules=[],
        packages=[
            "app.handlers",
            "app.routers",
        ]
    )

    # [App Base]
    config = providers.Configuration()
    config.from_pydantic(settings)

    # [Database]
    postgres_connection = providers.Singleton(PostgresConnection)
    db_session = providers.Factory(Session, postgres_connection=postgres_connection)

    # [Handlers]
    if settings.IS_DEV:
        demo_handler = providers.Factory(
            DemoHandler,
            session=db_session
        )

    user_handler = providers.Factory(
        UserHandler,
        session=db_session
    )
