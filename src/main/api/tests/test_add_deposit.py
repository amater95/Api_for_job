import pytest
from sqlalchemy.orm import Session

from src.main.api.classes.api_manager import ApiManager
from src.main.api.generators.model_generator import RandomModelGenerator
from src.main.api.models.add_deposit_request import AddDepositRequest
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.test_data.error_messages import ErrorMessages
from src.main.api.test_data.invalid_test_data import InvalidTestData
from src.main.api.db.crud.account_crud import AccountCrudDb as Account
from src.main.api.test_data.test_data import TestData


@pytest.mark.api
class TestAddDeposit:
    def test_add_deposit(self, db_session: Session, api_manager: ApiManager, create_user_request: CreateUserRequest, create_account_request):
        add_deposit_request = RandomModelGenerator.generate(AddDepositRequest, accountId = create_account_request.id)
        response = api_manager.user_steps.add_deposit(create_user_request, add_deposit_request)

        account_from_db = Account.get_one_from_db(db_session, id = create_account_request.id)

        assert response.balance == add_deposit_request.amount, f"После пополнения баланс должен быть равен {add_deposit_request.amount}, а остался {response.balance}"
        assert account_from_db.balance == add_deposit_request.amount, f"Баланс в БД {account_from_db.balance} не соответствует пополнению {add_deposit_request.amount}"



    @pytest.mark.parametrize("deposit", InvalidTestData.INVALID_DATA_FOR_DEPOSIT)
    def test_add_deposit_with_invalid_summ(self, db_session: Session, api_manager: ApiManager, create_user_request: CreateUserRequest, create_account_request, deposit: float):
        add_deposit_request = AddDepositRequest(accountId = create_account_request.id, amount = deposit)
        request = api_manager.user_steps.add_deposit_with_invalid_summ(create_user_request, add_deposit_request)

        account_from_db = Account.get_one_from_db(db_session, id = create_account_request.id)

        assert request.json()["error"] == ErrorMessages.INVALID_DEPOSIT_AMOUNT, f"Ожидали ошибку {ErrorMessages.INVALID_DEPOSIT_AMOUNT}, а была получена {request.json()['error']}"
        assert account_from_db.balance == TestData.START_DEPOSIT_AMOUNT, "На счет была зачислена невалидная сумма"
