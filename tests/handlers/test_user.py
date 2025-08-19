"""
User handler tests.
"""
import pytest

from app.handlers import UserHandler
from app.serializers.v1.user import UserRegister, UserLogin


@pytest.mark.asyncio
async def test_register(
    user_handler: UserHandler
):
    """
    Test user registration.
    """
    user_register_model = UserRegister(
        email="dummy@gmail.com",
        display_name="dummy",
        password="abcd1234",
    )
    response = await user_handler.register(model=user_register_model)
    assert response is not None
    assert response.id is not None
    assert response.email == user_register_model.email
    assert response.display_name == user_register_model.display_name

@pytest.mark.asyncio
async def test_login(
    user_handler: UserHandler
):
    """

    :param user_handler:
    :return:
    """
    user_login_model = UserLogin(
        email="dummy@gmail.com",
        password="abcd1234"
    )
    response = await user_handler.login(model=user_login_model)
    assert response is not None
