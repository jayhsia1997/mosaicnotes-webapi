"""
Test cases for container
"""
import asyncpg
import pytest

from app.container import Container
from app.libs.database import PostgresConnection


@pytest.mark.asyncio
async def test_connection_pool(
    postgres_pool: PostgresConnection
):
    """
    Test connection pool instance
    :param postgres_pool:
    :return:
    """
    pool = await postgres_pool._create_pool()
    assert pool is not None
    assert isinstance(pool, asyncpg.pool.Pool)


@pytest.mark.asyncio
async def test_connection_pool_parallel(
    container: Container,
):
    """
    Test connection pool with parallel requests
    :param container:
    :return:
    """
    connection = container.postgres_connection()
    session1 = container.db_session()
    session2 = container.db_session()

    # Execute queries on both sessions
    await session1.execute("SELECT 1")
    # Get pool and connection IDs for both sessions
    pool1_id = id(session1._pool) if session1._pool else None
    conn1_id = id(session1._conn) if session1._conn else None
    await session2.execute("SELECT 2")
    # Get pool and connection IDs for both sessions
    pool2_id = id(session2._pool) if session2._pool else None
    conn2_id = id(session2._conn) if session2._conn else None

    # Check if the sessions are pooled
    assert session1._use_pool, "Session 1 should be pooled"
    assert session2._use_pool, "Session 2 should be pooled"
    # Check if the sessions are closed
    assert not session1.is_closed, "Session 1 should not be closed"
    assert not session2.is_closed, "Session 2 should not be closed"
    assert session1 is not session2, "Sessions should be different"
    assert pool1_id == pool2_id, "Pools should be the same"
    assert conn1_id != conn2_id, "Connections should be different"
