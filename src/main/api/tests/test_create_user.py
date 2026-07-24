import pytest
from sqlalchemy.orm import Session

from src.main.api.classes.api_manager import ApiManager
from src.main.api.fixtures.api_fixture import api_manager
from src.main.api.generators.model_generator import RandomModelGenerator
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.db.crud.user_crud import UserCrudDb as User


@pytest.mark.api
class TestCreateUser:
    @pytest.mark.parametrize(
        "create_user_request",
        [RandomModelGenerator.generate(CreateUserRequest)],
    )
    def test_create_user(self, db_session: Session, api_manager: ApiManager, create_user_request: CreateUserRequest):
        response = api_manager.admin_steps.create_user(create_user_request)

        user_from_db = User.get_one_from_db(db_session, username = create_user_request.username)

        assert create_user_request.username == response.username, f"Пользователю должно было присвоиться имя {create_user_request.username} вместо {response.username} "
        assert create_user_request.role == response.role, f"Пользователю присвоилась роль {response.role} вместо передаваемой {create_user_request.role}"
        assert user_from_db.username == create_user_request.username, f"Пользователь {create_user_request.username} не был создан в БД"


    @pytest.mark.parametrize(
        "username, password",
        [
            ("абв", "Pass!sw0rd"),
            ("ab", "Pas!sw0rd"),
            ("abcabcabcabcabca", "Pas!sw0rd"),
            ("abc!", "Pass!sw0rd"),
            ("User1", "Pass!sw0rд"),
            ("User2", "Pa!sw0"),
            ("User3", "pass!sw0rd"),
            ("User4", "PASS!SW0RD"),
            ("User5", "Passsw0rd"),
            ("User6", "Pass!swrd")
        ]
    )
    def test_create_invalid_user(self, db_session: Session, username: str, password: str, api_manager: ApiManager):
        create_user_request = CreateUserRequest(username=username, password=password, role="ROLE_USER")
        api_manager.admin_steps.create_invalid_user(create_user_request)

        user_from_db = User.get_one_from_db(db_session, username = create_user_request.username)

        assert user_from_db is None, f"Пользователь был создан"
