import pytest
from sqlalchemy.orm import Session

from src.main.api.classes.api_manager import ApiManager
from src.main.api.db.crud.account_crud import AccountCrudDb as Account
from src.main.api.db.crud.user_crud import UserCrudDb as User
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.test_data.error_messages import ErrorMessages
from src.main.api.test_data.test_data import TestData


@pytest.mark.api
class TestCreateAccount:
    def test_create_account(self, db_session: Session, api_manager: ApiManager, create_user_request: CreateUserRequest):
        response = api_manager.user_steps.create_account(create_user_request)

        account_from_db = Account.get_one_from_db(db_session, id = response.id)

        assert response.balance == TestData.START_DEPOSIT_AMOUNT, f"При создании нового аккаунта его баланс должен быть = {TestData.START_DEPOSIT_AMOUNT}, а получили {response.balance}"
        assert account_from_db.id == response.id, "Аккаунт не добавлен в БД"


    def test_create_three_accounts(self, db_session: Session, api_manager: ApiManager, create_user_request: CreateUserRequest):
        api_manager.user_steps.create_account(create_user_request)
        api_manager.user_steps.create_account(create_user_request)
        response_third_account = api_manager.user_steps.create_third_account(create_user_request)

        user_from_db = User.get_one_from_db(db_session, username = create_user_request.username)
        count_account_from_db = Account.count(db_session, user_id = user_from_db.id)

        assert (response_third_account.json()["error"] == ErrorMessages.MAX_ACCOUNTS_LIMIT_REACHED), f"Ожидали получить ошибку {ErrorMessages.MAX_ACCOUNTS_LIMIT_REACHED}"
        assert count_account_from_db == TestData.MAX_COUNT_ACCOUNT, "Третий аккаунт пользователя создался в БД"
