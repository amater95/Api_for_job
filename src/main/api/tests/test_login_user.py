import pytest

from src.main.api.classes.api_manager import ApiManager
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.login_user_request import LoginUserRequest
from src.main.api.test_data.test_data import TestData
from src.main.api.test_data.secret_data import AdminData



@pytest.mark.api
class TestLoginUser:
    def test_login_admin(self, api_manager: ApiManager):
        login_admin_request = LoginUserRequest(username = AdminData.LOGIN, password = AdminData.PASSWORD)
        response = api_manager.admin_steps.login_user(login_admin_request)

        assert login_admin_request.username == response.user.username, f"Администратор имеет login = {login_admin_request.username}, а не = {response.user.username}"
        assert response.user.role == TestData.ADMIN_ROLE, f"Админ может иметь только роль = {TestData.ADMIN_ROLE}, но не = {response.user.role}"


    def test_login_user(self, api_manager: ApiManager, create_user_request: CreateUserRequest):
        response = api_manager.admin_steps.login_user(create_user_request)

        assert create_user_request.username == response.user.username, f"Пользователь должен иметь имя {create_user_request.username}, а не = {response.user.username}"
        assert response.user.role == TestData.USER_ROLE, f"Пользователь имеет роль {TestData.USER_ROLE}, вместо = {response.user.role}"
    