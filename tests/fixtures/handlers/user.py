"""
User Fixtures
"""
import pytest

@pytest.fixture
def user_handler(container):
    """
    User handler fixture.
    """
    return container.user_handler()
